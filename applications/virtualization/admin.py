from django.contrib import admin
from .models import (Area, Collaborator, Project, Provider, VM, Site, Tenant, Network, Descriptor, Todo, Port)
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db import models
from django.forms import TextInput
from admin_auto_filters.filters import AutocompleteFilter
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin


admin.site.site_header = "ADMIN | VIRTUALIZACION TCLOUD"
admin.site.site_title = "VIRTUALIZACION TCLOUD"

class TenantFilter(AutocompleteFilter):
    title = 'Tenant'
    field_name = 'tenant'

class SiteFilter(AutocompleteFilter):
    title = 'Site'
    field_name = 'site'

class PortFilter(AutocompleteFilter):
    title = 'network'
    field_name = 'network'

class TodoInline(NestedTabularInline):
    model = Todo
    extra = 10
    max_num = 10
    fields = ('line_number', 'todo_title', 'deadline_date', 'collaborator', 'done_date', 'state', 'ordering_position')
    readonly_fields = ('line_number',)
    ordering = ('ordering_position', )

    initial = [
        {'todo_title': 'Aprobación de recursos CAR/PAC','ordering_position': '1'},
        {'todo_title': 'Cesta en Compra','ordering_position': '2'},
        {'todo_title': 'Adjudicación ','ordering_position': '3'},
        {'todo_title': 'Adecuación de emplazamiento','ordering_position': '4'},
        {'todo_title': 'Infraestructura de Computo (TC)','ordering_position': '5'},
        {'todo_title': 'Delivery local','ordering_position': '6'},
        {'todo_title': 'Integraciones con otras redes ','ordering_position': '7'},
        {'todo_title': 'Pruebas funcionales','ordering_position': '8'},
        {'todo_title': 'Puesta en Servicio','ordering_position': '9'},
        {'todo_title': 'Acta de aceptación/ Generación de HEM','ordering_position': '10'},
    ]

    create_from_default = True

    def get_formset(self, request, obj=None, **kwargs):
        initial = self.initial[:]

        class _Form(forms.ModelForm):
            form_initial = initial

            def __init__(self, *args, **kwargs):
                if len(self.form_initial) and not 'instance' in kwargs:
                    kwargs['initial'] = self.form_initial.pop(0)
                return super(_Form, self).__init__(*args, **kwargs)

        if self.create_from_default:
            if request.method == 'GET':
                self.form = _Form
            else:
                self.form = forms.ModelForm
        else:
            self.form = _Form

        return super(TodoInline, self).get_formset(request, obj, **kwargs)

    line_numbering = 0
    def line_number(self, obj):
        self.line_numbering += 1
        return self.line_numbering

    line_number.short_description = '#'

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30%'})},
    }

class TodoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Todo._meta.get_fields()]

admin.site.register(Todo, TodoAdmin)

class PortInline(NestedTabularInline):
    model = Port
    extra = 0
    inline_classes = ('collapse', 'close',)
    autocomplete_fields = ['network', 'network__project__project_title']
    search_fields = ['network__network_name',]

class PortAdmin(admin.ModelAdmin):
    model = Port
    list_filter = [PortFilter]
    autocomplete_fields = ['network', ]

class VMInline(NestedTabularInline):
    model = VM
    extra = 0
    readonly_fields = ('line_number',)
    autocomplete_fields = ['tenant', ]
    inlines = [PortInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10%'})},
    }

    line_numbering = 0
    def line_number(self, obj):
        self.line_numbering += 1
        return self.line_numbering

    line_number.short_description = '#'

class VMResources(resources.ModelResource):
    class Meta:
        model = VM

class VMAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def date_format(self, obj):
        return obj.pub_date.strftime("%d-%b-%Y")

    date_format.short_description = "Fecha"

    def link(self, obj):
        return mark_safe('<a class="historylink" href="%s">Editar proyecto</a>' % \
                         reverse('admin:virtualization_project_change',
                                 args=(obj.id,)))

    model = VM
    resources_class = VMResources
    # list_display = ['vm_name', 'project', 'date_format', 'vcpu_total', 'ram_total', 'internal_disk_total', 'external_disk_total', 'tenant', 'site', 'link']
    list_display = ['vm_name', 'project', 'date_format', 'vcpu_total', 'ram_total', 'internal_disk_total', 'external_disk_total', 'tenant', 'link']

    list_filter = [TenantFilter, 'tenant__site']
    autocomplete_fields = ['tenant', ]

admin.site.register(VM, VMAdmin)

class CollaboratorInline(admin.TabularInline):
    model = Collaborator
    extra = 0

class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'area', 'get_responsable']
    list_filter = ['area__responsable', 'area__area_title']

    def get_responsable(self, obj):
        return obj.area.responsable
    get_responsable.short_description = 'Lider'
    get_responsable.admin_order_field = 'area__responsable'

admin.site.register(Collaborator, CollaboratorAdmin)

class AreaAdmin(admin.ModelAdmin):
    def collaborator_count(self, obj):
        return obj.collaborator_set.count()

    collaborator_count.short_description = 'Colaboradores'

    list_display = ['area_title', 'responsable', 'collaborator_count']
    inlines = [CollaboratorInline]

admin.site.register(Area, AreaAdmin)

class TenantResources(resources.ModelResource):
    class Meta:
        model = Tenant

class TenantAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    def vm_count(self, obj):
        return obj.vm_set.count()

    vm_count.short_description = 'VM'

    model = Tenant
    search_fields = ['tenant_hostname']
    list_display = ['tenant_hostname', 'site', 'ip_inband', 'ip_outband', 'vm_count']
    resources_class = TenantResources

admin.site.register(Tenant, TenantAdmin)

class SiteAdmin(admin.ModelAdmin):
    model = Site
    search_fields = ['site_name']
    list_display = ['site_name', 'id']

admin.site.register(Site, SiteAdmin)

class DescriptorInline(NestedTabularInline):
    model = Descriptor
    extra = 0

class NetworkInline(NestedTabularInline):
    model = Network
    extra = 0

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10%'})},
    }

class NetworkAdmin(admin.ModelAdmin):
    model = Network
    search_fields = ['network_name', 'project__project_title', 'site__site_name']

admin.site.register(Network, NetworkAdmin)

class ProjectAdmin(NestedModelAdmin):
    def vm_count(self, obj):
        return obj.vm_set.count()
    vm_count.short_description = 'VM'

    def net_count(self, obj):
        return obj.network_set.count()
    net_count.short_description = 'Redes'

    filter_horizontal = ('collaborator',)
    list_display = ['project_title', 'slug', 'country', 'provider', 'vm_count', 'net_count', 'state']
    save_on_top = True
    search_fields = ['project_title']
    inlines = [NetworkInline, VMInline, DescriptorInline, TodoInline, ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Provider)
