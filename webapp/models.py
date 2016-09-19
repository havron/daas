from django.db import models
import json

# User superclass
class User(models.Model):
    username = models.CharField()
    password = mdoels.CharField()
    email_address = models.EmailField()
    #TODO jobs #(list of all Job objects that belong to the user)

class Host(models.Model):
    host_reputation = models.FloatField()
    user = models.OneToOneField(User)
    #TODO drones_owned
    #TODO drones_available # (list of ready-to-lease drone objects in the owned list)
    #TODO drones_deployed # (list of drone objects out for lease in the owned list)

class Client(models.Model):
    client_reputation = models.FloatField()
    user = models.OneToOneField(User)

class Drone(models.Model):
    drone_id = models.CharField()
    model_name = models.CharField()
    drone_desc = models.TextField()
    demo_link = models.URLField # (link to photo gallery or videos)
    permissions = models.CharField()
    owner_email = models.EmailField()
    last_checked_out = models.DateTimeField()
    battery_level = models.FloatField()
    maintenance_status = models.TextField
    available_for_hire = models.BooleanField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    #TODO location (tuple(float, float))
    # picture = models.ImageField() (image format)

# [all of the subprocesses happening between client wanting a drone and drone returning to owner]
class Jobs(models.Model):
    transaction_id = models.CharField()
    drone_id = models.CharField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    price_per_day = models.FloatField() # [ask TAs how to do price, also just look at project descriptions to see what we need to do for this]
    transaction_time = models.DateTimeField()
    job_status_choices = ['cancelled', 'active', 'inactive']
    job_status = models.CharField(choices = job_status_choices)
    #TODO schedule (Schedule object)

class Schedule(models.Model): # [perhaps create superclass and have separate jobs/drone schedules]
    schedule_id = models.CharField()
    time_leased = models.DateTimeField()
    time_returned = models.DateTimeField()

#Client_Reputation: [to be determined. includes block cipher stuffs.]

#Host_Reputation: [to be determined. includes block cipher stuffs.]