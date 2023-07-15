from django import forms
from .models import ChatRoom


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name", "image", "description", "users"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["users"].widget.attrs["class"] = "select2"
        self.fields["users"].widget.attrs["multiple"] = True
