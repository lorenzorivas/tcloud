from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Provider(models.Model):
    provider_name = models.CharField(max_length=255, verbose_name='Proveedor')

    def __str__(self):
        return self.provider_name

    class Meta:
        ordering = ['-id']

class Site(models.Model):
    site_name = models.CharField(max_length=255, verbose_name='Sitio')

    def __str__(self):
        return self.site_name

    class Meta:
        ordering = ['-id']

class Tenant(models.Model):
    tenant_hostname = models.CharField(max_length=255, verbose_name='Hostname')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    ip_inband = models.GenericIPAddressField(blank=True, null=True)
    ip_outband = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.tenant_hostname

    class Meta:
        ordering = ['-id']

class Area(models.Model):
    area_title = models.CharField(max_length=255, verbose_name='Area')
    responsable = models.CharField(max_length=255, verbose_name='Lider Area')

    def __str__(self):
        return self.area_title

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['-id']

class Collaborator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Nombre')
    country = CountryField(blank_label='(seleccionar país)', verbose_name='País')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s %s" % ( self.user.first_name, self.user.last_name )

    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
        ordering = ['-id']

class Project(models.Model):
    project_title = models.CharField(max_length=200, verbose_name='Titulo')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Proveedor')
    year = models.IntegerField(null=True, verbose_name='Año Proyectado')
    country = CountryField(verbose_name='Pais')
    # slug = AutoSlugField(populate_from=lambda instance: "{0}-{1}".format(instance.project_title, instance.country), always_update=True, null=True)
    slug = AutoSlugField(populate_from='project_title_country', always_update=True, null=True)
    collaborator = models.ManyToManyField(Collaborator, related_name='Colaborador', verbose_name='Colaboradores')
    resume = HTMLField()
    pub_date = models.DateTimeField(auto_now_add=True)
    planned_date = models.DateField(null=True, verbose_name='Fecha Planificada')
    done_date = models.DateField(null=True, verbose_name='Fecha de termino Real', blank=True)
    state = models.BooleanField(blank=True, null=True, default=False, verbose_name='Terminando?')

    def project_title_country(self):
        return '%s %s' % (self.project_title, self.country.name)

    def __str__(self):
        return '%s %s' % (self.project_title, self.country)

    class Meta:
        verbose_name = 'Proyecto'
        ordering = ['-id']

class VM(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vm_name = models.CharField(max_length=200, verbose_name='Nombre VM')
    slug = AutoSlugField(populate_from='vm_name', always_update=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(blank=True, null=True, default=False, verbose_name='Activa')
    vcpu_total = models.IntegerField(null=True, verbose_name='vCPU')
    ram_total = models.IntegerField(null=True, verbose_name='RAM')
    internal_disk_total = models.IntegerField(null=True, verbose_name='Disco IN')
    external_disk_total = models.IntegerField(null=True, blank=True, verbose_name='Disco EX')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.vm_name

    class Meta:
        verbose_name = 'Virtual Machine'
        ordering = ['id']

class Network(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    network_name = models.CharField(max_length=200, verbose_name='Nombre')
    ip_address_mask = models.CharField(max_length=200, verbose_name='IP/MASK')
    vlan_id = models.CharField(max_length=200, verbose_name='VLAN')
    vrrp_vip = models.GenericIPAddressField(blank=True, null=True)
    vrrp_r1 = models.GenericIPAddressField(blank=True, null=True)
    vrrp_r2 = models.GenericIPAddressField(blank=True, null=True)
    vrf_name = models.CharField(max_length=200, verbose_name='VRF')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.site, self.project, self.network_name)

class Port(models.Model):
    vm = models.ForeignKey(VM, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    ip_add = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.ip_add

class Descriptor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    descriptor_name = models.CharField(max_length=200, verbose_name='Titulo')
    descriptor = HTMLField()

class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    todo_title = models.CharField(max_length=200, verbose_name='Titulo')
    slug = AutoSlugField(populate_from='todo_title', always_update=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateField(null=True, verbose_name='Fecha planificación')
    collaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE, verbose_name='Encargado',null=True, blank=True)
    done_date = models.DateField(null=True, verbose_name='Fecha termino', blank=True)
    state = models.BooleanField(blank=True, null=True, default=False, verbose_name='Terminado')
    progress = models.IntegerField(blank=True, null=True, default=0)
    ordering_position = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.todo_title

    class Meta:
        verbose_name = 'Tareas de Proyecto'
        ordering = ['ordering_position']

    def diff_days(self):
        delta = self.deadline_date - self.done_date
        # print(delta.days)
        return delta.days > -5
