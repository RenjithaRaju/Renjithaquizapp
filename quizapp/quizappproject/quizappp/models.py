from django.db import models

# Create your models here.
class user_register(models.Model):
     username=models.CharField(max_length=200,default='')
     email=models.CharField(max_length=200,default='')
     phone=models.CharField(max_length=200,default='')
     course=models.CharField(max_length=200,default='')
     std_type=models.CharField(max_length=200,default='')
     logintime=models.CharField(max_length=200,default='')


     def __str__(self):
          return self.username


class questions(models.Model):
     question=models.CharField(max_length=500,default='')
     opt1=models.CharField(max_length=200,default='')
     opt2=models.CharField(max_length=200,default='')
     opt3=models.CharField(max_length=200,default='')
     opt4=models.CharField(max_length=200,default='')
     ans=models.CharField(max_length=200,default='')


     def __str__(self):
       return self.question
     


class Quizresult(models.Model):
    quiz_id=models.ForeignKey(user_register,on_delete=models.CASCADE,blank=True,null=True)
    quiz_score=models.IntegerField(blank=False,null=False,default=0)
    quiz_percent=models.IntegerField(blank=False,null=False,default=0)
    quiz_cottect=models.IntegerField(blank=False,null=False,default=0)
    quiz_wrong=models.IntegerField(blank=False,null=False,default=0)
    quiz_total=models.IntegerField(blank=False,null=False,default=0)
    quiz_date=models.CharField(max_length=200,default='')
    quiz_time=models.CharField(max_length=200,default='')

    def __str__(self):
        return str(self.quiz_id)
     