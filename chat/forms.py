from django import forms
from .models import ChatRoom

tag_style = """
    font-size: 1rem;
    font-weight: normal;
    color: #333;
    background-color: #fff;
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    width: 100%;
    height: 70px;
"""


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name", "image", "description", "users"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["users"].widget.attrs["class"] = "select2"
        self.fields["users"].widget.attrs["multiple"] = True
        self.fields["users"].widget.attrs["data-placeholder"] = "Select users"
        self.fields["users"].widget.attrs["style"] = tag_style
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = "Enter Chat Name"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs[
            "placeholder"
        ] = "Enter Chat Description"
        self.fields["image"].widget.attrs["class"] = "form-control"
