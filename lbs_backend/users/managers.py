from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, mobileNumber, idNumber, firstName, password=None):
        if not mobileNumber:
            raise ValueError('you must enter your MobileNumber')
        if not idNumber:
            raise ValueError('you must enter your IDNumber')
        if not firstName:
            raise ValueError('you must enter your FirstName')

        user = self.model(
            mobileNumber=mobileNumber,
            idNumber=idNumber,
            firstName=firstName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobileNumber, idNumber, firstName, password=None):
        user = self.create_user(mobileNumber, idNumber, firstName, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
