from django.db import models

# User superclass
class User(models.Model):
    username = models.CharField()
    password = mdoels.CharField()
    email_address = models.EmailField()
    #TODO many-to-many relationship with Host (sic)
    #TODO many-to-many relationship with Client (sic)
    #TODO jobs #(list of all Job objects that belong to the user)

class Host(models.Model):
    host_reputation = models.FloatField() # [did I lease the drones well?]
    #TODO drones_owned # (list of all the host's drone objects)
    #TODO drones_available # (list of ready-to-lease drone objects in the owned list)
    #TODO drones_deployed # (list of drone objects out for lease in the owned list)
    user = models.ManyToManyField(User) # ?

class Client(models.Model):
    client_reputation = models.FloatField() # [did I treat the drones well?]
    user = models.ManyToManyField(User) # ?

class Drone(models.Model):
    drone_id = models.CharField() # [each instance of drone object has a unique id]
    model_name = models.CharField()
    drone_desc = models.TextField() # [the host can enter whatever description they want]
    # picture = models.ImageField() (image format)
    demo_link = models.URLField # (link to photo gallery or videos)
    permissions = models.CharField() # [e.g. you can't edit my drone's software, you must comply to this government regulation, etc]
    #TODO - owner (User object) # [one owner per drone object]
    owner_email = models.EmailField()
    last_checked_out = models.DateTimeField() # [timestamp]
    #TODO location (tuple(float, float))
    battery_level = models.FloatField()
    maintenance_status = models.TextField # [owner writes in maintenance issues etc]
    available_for_hire = models.BooleanField() #[is it available right now, or is it not?]

# [all of the subprocesses happening between client wanting a drone and drone returning to owner]
class Jobs(models.Model):
    transaction_id = models.CharField()
    drone_id = models.CharField()
    #TODO host (Host object)
    #TODO client (Client object)
    price_per_day = models.FloatField() # [ask TAs how to do price, also just look at project descriptions to see what we need to do for this]
    transaction_time = models.DateTimeField()
    # job_status [cancelled, active, inactive, eaten by dog etc. could be a list of some sort]
    job_status_choices = ['cancelled', 'active', 'inactive']
    job_status = models.CharField(choices = job_status_choices) # ?
    #TODO schedule (Schedule object)

class Schedule(models.Model): # [perhaps create superclass and have separate jobs/drone schedules]
    schedule_id = models.CharField()
    time_leased = models.DateTimeField()
    time_returned = models.DateTimeField()

#Client_Reputation: [to be determined. includes block cipher stuffs.]

#Host_Reputation: [to be determined. includes block cipher stuffs.]