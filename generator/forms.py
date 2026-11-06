from django import forms

class CertificateGenerationForm(forms.Form):
    template = forms.ImageField(
        label="Certificate template",
        help_text="Upload a PNG or JPG certificate background."
    )
    participants = forms.FileField(
        label="Participant CSV",
        help_text="CSV file must include a column named 'name'."
    )
    name_x = forms.IntegerField(label="Name center X", min_value=0, initial=900)
    name_y = forms.IntegerField(label="Name center Y", min_value=0, initial=600)
    font_size = forms.IntegerField(label="Name font size", min_value=8, max_value=300, initial=54)
    text_color = forms.CharField(label="Name color", initial="#202020", max_length=7)
    font_file = forms.FileField(
        label="Optional .ttf font",
        required=False,
        help_text="Upload a TrueType font for better typography."
    )
    extra_fields = forms.CharField(
        label="Additional CSV fields (optional)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: column|x|y|font_size|#hexcolor"
    )

    def clean_text_color(self):
        value = self.cleaned_data["text_color"]
        if len(value) != 7 or not value.startswith("#"):
            raise forms.ValidationError("Use a hex color such as #202020.")
        try:
            int(value[1:], 16)
        except ValueError:
            raise forms.ValidationError("Enter a valid hex color.")
        return value

    def clean_font_file(self):
        file = self.cleaned_data.get("font_file")
        if file and not file.name.lower().endswith(".ttf"):
            raise forms.ValidationError("Please upload a .ttf font file.")
        return file
