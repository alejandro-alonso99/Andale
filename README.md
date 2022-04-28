# Andale
## What does this WebApp do?
Ándale is an accounting and billing web app that I created for a local taco restaurant, it includes features
such as a bill-printing section, as well as sales and expenses registration systems.

## Sections:

* **Productos:** Allows you to create product objects, you can  also see a list of the registered products and change the products' sale price by category.
* **Gastos:** Allows you to register the shops' expenses, you can also see a list of the registered expenses.
* **Delivery:** Here you can register a delivery sale, you can add products to the sale through a form, an the print a receipt for the sale.
* **Mesas:** In this section the user can "open" restaurant tables and then register products for the table. You can then close the sale and print a receipt.
* **Sales:** Here you can see all the sales that the user registerer thrugh the Delivery and Mesas sections.
* **Resumenes:** Here you can see a daily and monthly summary for sales and expenses.

This webapp works for multiple users, so that every separate franchise of the company can use the software independently. The users log-in through a login view.

## This project Includes:

## Tables managing view:
In this view you can "open" tables, add products to them, and then print a receipt. In this case the user opens table number 1 and adds products, then he prints the receipt and later closes the sale wich is payed in cash. This sale get's registered in the database.
![gif](tables.gif)

## Receipts:
# This is the receipt that got printed in the last sale.
<img src="receipt.jpeg" alt="receipt" width="400"/>

## Create views:
Create views include forms that let you create objects. In this case this user created a product named Taco de carne.
![gif](create_product.gif)

## List views:
List views let you see all registered objects of a given kind, you can also for example change the price of all products of a specified category. In this case the user raises the price of all food products by a 10%.
![gif](products_list.gif)

## Detail views:
Detail views give you information about the given object, you can also delete the object or change a product's sale price.
![detail_view](detail_view.png)


