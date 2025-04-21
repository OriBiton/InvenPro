import os
import io
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrderForm
from django.http import FileResponse
from django.utils.timezone import now
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import io
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
import os
from.models import Order
from inventory.models import Product
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.http import require_http_methods
from django.contrib import messages
# רישום הגופן לעברית
FONT_PATH = os.path.join('static', 'fonts', 'FreeSans.ttf')
pdfmetrics.registerFont(TTFont('Hebrew', FONT_PATH))


@login_required
def create_order_view(request):
    if not request.user.is_approved:
        return redirect('login')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
             # שמירה לדאטהבייס
            order = Order.objects.create(
                customer_name=data['customer_name'],
                phone_number=data['phone_number'],
                address=data['address'],
                model=data['model'],
                description=data['description'],
                total_price=data['total_price'],
                deposit_paid=data['deposit_paid'],
                measure=data['measure']
            )
            # יצירת PDF בזיכרון
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            # הוספת לוגו
            logo_path = os.path.join('static', 'media', 'oristone.png') # ודא שהתמונה שמורה שם
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, x=160, y=height - 100, width=280, height=60, mask='auto')  # למעלה, באמצע

            # הגדרות טקסט
            # הגדרות טקסט
            c.setFont("Hebrew", 14)

            y = height - 150  # תחילת טקסט אחרי הלוגו
            line_height = 28

            labels = [
                ("הזמנה עבור:", data['customer_name'][::-1]),
                ("טלפון:", data['phone_number']),
                ("כתובת:", data['address'][::-1]),
                ("דגם:", data['model']),
                ("תיאור:", data['description'][::-1]),
                ("סכום לתשלום:", f'ח"ש {data["total_price"]} '),
                ("מקדמה:", f'ח"ש  {data["deposit_paid"]}'),
                ("מדידה:", f'ח"ש  {data["measure"]}'),
                ("תאריך הזמנה:", now().strftime('%d/%m/%Y')),
                ("חתימה:", '_________________________')
            ]

            for label, value in labels:
                full_line = f"{value} {label[::-1]}"
                c.drawRightString(550, y, full_line)
                y -= line_height
                if label!="חתימה:":
                    c.line(50, y + 10, 550, y + 10)  # קו הפרדה
                y -= 10

            c.showPage()
            c.save()
            buffer.seek(0)

            filename = f"{data['customer_name']}_order_{now().strftime('%Y%m%d%H%M%S')}.pdf"
            # שמירת ה-PDF לקובץ זמני
            pdf_path = os.path.join('media', 'pdf_orders', filename)
            with open(pdf_path, 'wb') as f:
                f.write(buffer.read())

            # הפניה לעמוד שמציג את המלאי + קישור ל-PDF
            

            url = reverse('inventory_by_model', kwargs={'model': data['model']})
            query_string = urlencode({'pdf': filename})
            full_url = f"{url}?{query_string}"
            return redirect(full_url)



    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def inventory_by_model_view(request, model):
    products = Product.objects.filter(model=model, count__gt=0)
    pdf_filename = request.GET.get('pdf')

    if request.method == 'POST':
        for product in products:
            raw_value = request.POST.get(f'use_{product.id}', '').strip()
            if raw_value.isdigit():
                used_qty = int(raw_value)
                if 0 < used_qty <= product.count:
                    product.count -= used_qty
                    product.save()
                if product.count == 0:
                    product.delete()
        messages.success(request, "המלאי עודכן בהצלחה.")
        return redirect(request.path + f'?pdf={pdf_filename}')

    return render(request, 'orders/products_by_model.html', {
        'model': model,
        'products': products,
        'pdf_filename': pdf_filename,
    })
