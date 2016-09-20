from django.db import models
import json

# User superclass
class User(models.Model):

    # some type of hash
    user_id = models.IntField()

    username = models.CharField()
    def __setUsername__(self, username, val):
        super(User, self).__setUsername__(username, val)
    def __getUsername__(self, username):
        return super(User, self).__getUsername__(username)
    #TODO def __str__(self) for returning string

    password = mdoels.CharField()
    def __setPassword__(self, password, val):
        super(User, self).setPassword__(password, val)
    def __getPassword__(self, password):
        return super(User, self).__getPassword__(password)

    email_address = models.EmailField()
    def __setEmailAddress__(self, email_address, val):
        super(User, self).setEmailAddress__(email_address, val)
    def __getEmailAddress__(self, email_address):
        return super(User, self).__getEmailAddress__(email_address)
    #TODO jobs #(list of all Job objects that belong to the user)


# Host subclass extends from User class
class Host(models.Model):

    # calculation based on specific equation
    host_reputation = models.FloatField()
    user = models.OneToOneField(User)
    drones_owned = models.OneToManyField(Drone)
    drones_available = models.OneToManyField(Drone)
    drones_deployed = models.OneToManyField(Drone)


# Client subclass extends from User class
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
