"""Checkout calculator: integer rupiah, vouchers, and delivery fees."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    name: str
    price: int
    quantity: int = 1

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Item name is required")
        if type(self.price) is not int or self.price < 0:
            raise ValueError("Price must be a nonnegative integer")
        if type(self.quantity) is not int or self.quantity < 1:
            raise ValueError("Quantity must be a positive integer")

    @property
    def subtotal(self):
        return self.price * self.quantity


@dataclass(frozen=True)
class OrderSummary:
    subtotal: int
    discount: int
    shipping: int
    total: int


VOUCHERS = {"HEMAT10": 10, "HEMAT20": 20}
FREE_SHIPPING_MINIMUM = 100_000
SHIPPING_FEE = 15_000


def checkout(items, voucher=""):
    """Free shipping is based on the amount AFTER discount."""
    if not items:
        raise ValueError("Cart cannot be empty")
    code = voucher.strip().upper()
    if code and code not in VOUCHERS:
        raise ValueError("Unknown voucher")

    subtotal = sum(item.subtotal for item in items)
    discount = subtotal * VOUCHERS.get(code, 0) // 100
    discounted_subtotal = subtotal - discount
    shipping = 0 if discounted_subtotal >= FREE_SHIPPING_MINIMUM else SHIPPING_FEE
    total = discounted_subtotal + shipping
    return OrderSummary(subtotal, discount, shipping, total)


if __name__ == "__main__":
    cart = [CartItem("Mechanical keyboard", 80_000), CartItem("Desk mat", 40_000)]
    summary = checkout(cart, "HEMAT10")
    print("BUILD / LIGHT STORE — CHECKOUT")
    for item in cart:
        print(f"{item.name} x{item.quantity}: Rp{item.subtotal:,}")
    print(f"Subtotal : Rp{summary.subtotal:,}")
    print(f"Discount : Rp{summary.discount:,}")
    print(f"Shipping : Rp{summary.shipping:,}")
    print(f"TOTAL    : Rp{summary.total:,}")
