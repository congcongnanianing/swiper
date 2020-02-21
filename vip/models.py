from django.db import models

# Create your models here.


class Vip(models.Model):
    name = models.CharField(max_length=16,unique=True)
    level = models.IntegerField(unique=True)
    price = models.FloatField()

    class Meta:
        ordering = ['level']

    def permissions(self):
        '''当前vip具有的权限信息'''
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_ids = [relation.perm_id for relation in relations]
        return Permission.objects.filter(id__in=perm_ids)
        '''这里如果使用外键的化可以只进行一次数据库的查询，但是外键很影响性能；如果要做优化可以写原生的SQL或将多对多的关系放进缓存里面'''

    def has_perm(self,perm_name):
        '''检查该等级VIP是否具有某权限'''
        try:
            perm = Permission.get(name=perm_name)
        except Permission.DoesNotExist:
            return False
        else:
            return VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()


class Permission(models.Model):
    name = models.CharField(max_length=32,unique=True)
    desc = models.TextField()   # 权限描述


# Vip 和 Permission是多对多多关系，这个表是它们的关系表
class VipPermRelation(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
