from django.db import models


class Inquiry(models.Model):
    inquiry_id = models.AutoField(
        primary_key=True
    )
    
    prompt = models.TextField(
        default=None
    )
    
    images = models.ImageField(
        default=None,
        upload_to='media/'
    )
    
    rounds = models.IntegerField(
        default=1
    )
    
    def __str__(self):
        return f"ID #{self.inquiry_id} ({self.rounds} rounds): {self.prompt}"
    
    def serialize(self):
        return {
            "id" : self.inquiry_id,
            "prompt" : self.prompt,
            "images" : self.images,
            "rounds" : self.rounds
        }
  
    
class Response(models.Model):
    response_id = models.AutoField(
        primary_key=True
    )
    
    # True -> Given by the LLM responsible for answering prompts
    # False -> Given by the LLM responsible for giving further insights
    is_answer = models.BooleanField()
    
    content = models.TextField(
        default=None
    )
    
    def __str__(self):
        response_type = "Answer" if self.is_answer else "Insight"
        return f"ID #{self.response_id} ({response_type}): {self.content}"
    