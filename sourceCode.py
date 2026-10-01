import datetime
import random


class Product:

    def __init__(self, product_id, name, stock, reorder_point, max_capacity):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.reorder_point = reorder_point  # آستانه سفارش مجدد
        self.max_capacity = max_capacity  # حداکثر ظرفیت نگهداری

    def __str__(self):
        status = (
            "⚠️ نیاز به سفارش"
            if self.stock <= self.reorder_point
            else "✅ وضعیت عادی"
        )
        return f"کد: {self.product_id} | نام: {self.name:<12} | موجودی: {self.stock:<4} | وضعیت: {status}"


class InventorySystem:

    def __init__(self):
        self.products = {}
        self.transactions = []

    def add_product(self, product_id, name, initial_stock, reorder_point, max_capacity):
        if product_id in self.products:
            print("❌ خطا: کالایی با این کد قبلاً ثبت شده است.")
            return False
        product = Product(
            product_id, name, initial_stock, reorder_point, max_capacity
        )
        self.products[product_id] = product
        self._record_transaction(product_id, "ثبت اولیه", initial_stock)
        print(f"✅ کالای '{name}' با موفقیت تعریف شد.")
        return True

    def update_stock(self, product_id, quantity, trans_type):
        """ثبت ورود (IN) یا خروج (OUT) کالا"""
        if product_id not in self.products:
            print("❌ خطا: کالا یافت نشد!")
            return False

        product = self.products[product_id]

        if trans_type.upper() == "IN":
            if product.stock + quantity > product.max_capacity:
                print(
                    f"⚠️ warning: افزودن این تعداد، بیشتر از حداکثر ظرفیت انبار ({product.max_capacity}) است!"
                )
            product.stock += quantity
            self._record_transaction(product_id, "ورود به انبار", quantity)
            print(f"✅ تعداد {quantity} عدد به موجودی {product.name} اضافه شد.")

        elif trans_type.upper() == "OUT":
            if product.stock < quantity:
                print(
                    f"❌ خطا: موجودی کافی نیست! (موجودی فعلی: {product.stock})"
                )
                return False
            product.stock -= quantity
            self._record_transaction(product_id, "خروج از انبار", quantity)
            print(f"✅ تعداد {quantity} عدد از {product.name} کسر شد.")

            if product.stock <= product.reorder_point:
                print(
                    f"🔔 هشدار: موجودی {product.name} به نقطه سفارش مجدد ({product.stock}) رسید!"
                )

        return True

    def _record_transaction(self, product_id, trans_type, quantity):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "timestamp": timestamp,
            "product_id": product_id,
            "type": trans_type,
            "quantity": quantity,
        })

    def display_inventory(self):
        print("\n" + "=" * 55)
        print("📋 گزارش وضعیت موجودی انبار")
        print("=" * 55)
        if not self.products:
            print("هیچ کالایی در انبار ثبت نشده است.")
        for product in self.products.values():
            print(product)
        print("=" * 55)

    def simulate_demand(self, product_id, days=15):
        """شبیه‌سازی تقاضای تصادفی روزانه برای یک کالا در چند روز آینده"""
        if product_id not in self.products:
            print("❌ کالا یافت نشد.")
            return

        product = self.products[product_id]
        print(f"\n🎲 شروع شبیه‌سازی تقاضا برای '{product.name}' طی {days} روز:")
        print(
            f"موجودی اولیه: {product.stock} | نقطه سفارش مجدد: {product.reorder_point}\n"
        )

        sim_stock = product.stock
        stockouts = 0

        for day in range(1, days + 1):
            # شبیه‌سازی تقاضای تصادفی بین ۰ تا ۱۵ عدد در روز
            daily_demand = random.randint(0, 15)

            if sim_stock >= daily_demand:
                sim_stock -= daily_demand
                status = f"فروش: {daily_demand:<2} -> موجودی مانده: {sim_stock:<3}"
            else:
                stockouts += 1
                status = f"❌ کمبود موجودی! (تقاضا: {daily_demand} | موجودی: {sim_stock})"
                sim_stock = 0

            # بررسی نیاز به سفارش مجدد
            reorder_flag = " (📢 زمان سفارش مجدد!)" if sim_stock <= product.reorder_point else ""
            print(f"روز {day:<2}: {status}{reorder_flag}")

        print("-" * 55)
        print(
            f"📊 نتیجه شبیه‌سازی: تعداد روزهای مواجه شده با کمبود کالا: {stockouts} روز"
        )


# ==========================================
# منوی تعاملی اجرا
# ==========================================
def main():
    inventory = InventorySystem()

    # چند داده پیش‌فرض برای تست سریع
    inventory.add_product("P101", "لپ‌تاپ", initial_stock=20, reorder_point=5, max_capacity=50)
    inventory.add_product("P102", "ماوس", initial_stock=50, reorder_point=15, max_capacity=100)

    while True:
        print("\n--- سیستم مدیریت و شبیه‌سازی انبار ---")
        print("1. مشاهده وضعیت موجودی انبار")
        print("2. تعریف کالای جدید")
        print("3. ثبت ورود/خروج کالا")
        print("4. شبیه‌سازی تقاضا و مصرف کالا (Monte Carlo)")
        print("5. خروج")

        choice = input("لطفاً یک گزینه را انتخاب کنید (1-5): ")

        if choice == "1":
            inventory.display_inventory()

        elif choice == "2":
            pid = input("کد کالا: ")
            name = input("نام کالا: ")
            stock = int(input("موجودی اولیه: "))
            reorder = int(input("آستانه سفارش مجدد: "))
            capacity = int(input("حداکثر ظرفیت انبار برای این کالا: "))
            inventory.add_product(pid, name, stock, reorder, capacity)

        elif choice == "3":
            pid = input("کد کالا: ")
            ttype = input("نوع تراکنش (IN برای ورود / OUT برای خروج): ")
            qty = int(input("تعداد: "))
            inventory.update_stock(pid, qty, ttype)

        elif choice == "4":
            pid = input("کد کالا برای شبیه‌سازی: ")
            days = int(input("تعداد روزهای شبیه‌سازی (مثلاً 15): "))
            inventory.simulate_demand(pid, days)

        elif choice == "5":
            print("با تشکر! برنامه پایان یافت.")
            break
        else:
            print("گزینه نامعتبر است.")


if __name__ == "__main__":
    main()