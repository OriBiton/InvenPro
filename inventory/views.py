from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Product
from datetime import datetime
from django.contrib import messages  # נוסיף אם עדיין אין
from django.utils import timezone



@login_required
def inventory_view(request):
    if not request.user.is_approved:
        return redirect('login')

    products = Product.objects.filter(count__gt=0)


    # חיפוש חכם
    model_query = request.GET.get('model')
    date_query = request.GET.get('date')

    if model_query:
        products = products.filter(model__icontains=model_query)
    if date_query:
        products = products.filter(date=date_query)
    products = products[:5]
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            model = request.POST.get("model")
            type = request.POST.get("type")
            height = request.POST.get("height")
            width = request.POST.get("width")

            # בדיקת שדות חובה
            if not model or not type or not height or not width:
                messages.error(request, "יש למלא את כל השדות החובה: דגם, סוג, גובה, רוחב.")
                return redirect("inventory")

            # שדות לא חובה עם ערך ברירת מחדל
            deploying_number = request.POST.get("deploying_number", "")
            count = int(request.POST.get("count") or 1)
            date_str = request.POST.get("date")
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else timezone.now().date()
            except ValueError:
                messages.error(request, "תאריך שגוי.")
                return redirect("inventory")

            height = 160 if type == "פלטה" else float(height)
            width = 320 if type == "פלטה" else float(width)

            # בדוק אם כבר קיים
            existing = Product.objects.filter(
                model=model,
                deploying_number=deploying_number,
                date=date_obj,
                height=height,
                width=width,
                type=type
            ).first()

            if existing:
                existing.count += count
                existing.save()
            else:
                Product.objects.create(
                    model=model,
                    deploying_number=deploying_number,
                    date=date_obj,
                    height=height,
                    width=width,
                    type=type,
                    count=count
                )

            messages.success(request, "המוצר נוסף בהצלחה.")
            return redirect("inventory")

        elif action == "use":
            product_id = int(request.POST.get("product_id"))
            amount = int(request.POST.get("amount", 1))
            product = get_object_or_404(Product, id=product_id)

            if product.count > amount:
                product.count -= amount
                product.save()
            else:
                product.delete()

            messages.success(request, "המוצר עודכן או הוסר בהצלחה.")
            return redirect("inventory")

    return render(request, "inventory/inventory.html", {"products": products})
