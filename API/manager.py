from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required!")

        #normalizing email
        email = self.normalize_email(email)
        
        # creating and storing user
        user = self.model(email=email, **kwargs)
        # storing password as hash
        user.set_password(password)
        # saving user to db
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        # setting some default values which is required when creating superuser
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)

        return self.create_user(email,password, **kwargs)