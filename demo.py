'''


### Question 1: Are Django signals executed synchronously or asynchronously by default?

**Answer:**

By default, Django signals are executed **synchronously**. This means that when a signal is triggered, Django waits for the connected functions (handlers) to complete before continuing. 

Here's a simple example:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal received for:", instance.name)

# Creating an instance of MyModel
obj = MyModel.objects.create(name="Test")
print("Object created")
```

Explanation:  
When we create a `MyModel` object, the signal `post_save` is triggered, and `my_signal_handler` runs immediately (synchronously). The print statement "Object created" only happens **after** the signal handler finishes.

---

### Question 2: Do Django signals run in the same thread as the caller?

**Answer:**

Yes, by default, Django signals run in the **same thread** as the caller. 

Here's a simple example to show this:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import threading

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal received for:", instance.name)
    print("Signal handler thread ID:", threading.get_ident())

# Creating an instance of MyModel
obj = MyModel.objects.create(name="Test")
print("Main thread ID:", threading.get_ident())
```

Explanation:  
When we create an object of `MyModel`, the signal handler runs in the **same thread** as the caller. You can see this because the thread IDs for both the signal handler and the main code are the same.

---

### Question 3: Do Django signals run in the same database transaction as the caller?

**Answer:**

Yes, by default, Django signals run in the **same database transaction** as the caller. This means if the caller is in a transaction, the signal handler will be part of it too.

Here's a simple example:

```python
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal received for:", instance.name)
    instance.name = "Modified"
    instance.save()

# Creating an instance of MyModel
obj = MyModel.objects.create(name="Original")
print("Object name after save:", obj.name)
```

Explanation:  
In this example, when we save the object, the signal handler modifies the name to "Modified." Since the signal runs in the same transaction, the changes are part of the same operation. This ensures consistency.

'''