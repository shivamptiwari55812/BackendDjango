# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class App1Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=20)
    productname = models.CharField(db_column='ProductName', max_length=100)  # Field name made lowercase.
    productcategory = models.CharField(db_column='ProductCategory', max_length=100)  # Field name made lowercase.
    productquantity = models.IntegerField(db_column='ProductQuantity')  # Field name made lowercase.
    productprice = models.FloatField(db_column='ProductPrice')  # Field name made lowercase.
    product_rejected = models.IntegerField(db_column='Product_Rejected')  # Field name made lowercase.
    transaction_type = models.CharField(db_column='Transaction_type', max_length=30)  # Field name made lowercase.
    productrestock = models.IntegerField(db_column='ProductRestock', blank=True, null=True)  # Field name made lowercase.
    warehouse = models.ForeignKey('RegistrationWarehouse', models.DO_NOTHING, db_column='Warehouse_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'app1_inventory'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InboundSendersside(models.Model):
    id = models.BigAutoField(primary_key=True)
    sendercompany_name = models.CharField(db_column='SenderCompany_Name', max_length=100)  # Field name made lowercase.
    sender_address = models.CharField(db_column='Sender_Address', max_length=200)  # Field name made lowercase.
    sender_city = models.CharField(db_column='Sender_City', max_length=30)  # Field name made lowercase.
    sender_email = models.CharField(db_column='Sender_Email', max_length=100)  # Field name made lowercase.
    warehouse = models.ForeignKey('RegistrationWarehouse', models.DO_NOTHING, db_column='Warehouse_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inbound_sendersside'


class InvoiceInvoicebill(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_number = models.CharField(db_column='Invoice_number', max_length=100)  # Field name made lowercase.
    bill_date = models.DateField(db_column='Bill_date')  # Field name made lowercase.
    bill_number = models.CharField(db_column='Bill_number', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bill_time = models.DateTimeField(db_column='Bill_time')  # Field name made lowercase.
    bill_validity = models.DateField(db_column='Bill_validity')  # Field name made lowercase.
    valueofgoods = models.IntegerField(db_column='ValueOfGoods')  # Field name made lowercase.
    reasonfortransport = models.TextField(db_column='ReasonForTransport')  # Field name made lowercase.
    cewbno = models.IntegerField(db_column='CEWBno')  # Field name made lowercase.
    multivehinfo = models.IntegerField(db_column='MultiVehInfo')  # Field name made lowercase.
    bill_pdf = models.CharField(db_column='Bill_pdf', max_length=100)  # Field name made lowercase.
    receiver = models.ForeignKey('OutboundReceiverside', models.DO_NOTHING, db_column='Receiver_id', blank=True, null=True)  # Field name made lowercase.
    sender = models.ForeignKey(InboundSendersside, models.DO_NOTHING, db_column='Sender_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invoice_invoicebill'


class OutboundReceiverside(models.Model):
    id = models.BigAutoField(primary_key=True)
    receivercompany_name = models.CharField(db_column='ReceiverCompany_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    receiver_address = models.CharField(db_column='Receiver_Address', max_length=100)  # Field name made lowercase.
    receiver_city = models.CharField(db_column='Receiver_City', max_length=30)  # Field name made lowercase.
    receiver_gstin = models.CharField(db_column='Receiver_GSTIN', max_length=100)  # Field name made lowercase.
    receiver_state = models.CharField(db_column='Receiver_State', max_length=100)  # Field name made lowercase.
    receiver_contact = models.CharField(db_column='Receiver_Contact', max_length=30)  # Field name made lowercase.
    receiver_email = models.CharField(db_column='Receiver_Email', max_length=100)  # Field name made lowercase.
    modeoftransport = models.CharField(db_column='ModeOfTransport', max_length=100, blank=True, null=True)  # Field name made lowercase.
    warehouse = models.ForeignKey('RegistrationWarehouse', models.DO_NOTHING, db_column='Warehouse_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'outbound_receiverside'


class RegistrationOtp(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'registration_otp'


class RegistrationWarehouse(models.Model):
    id = models.BigAutoField(primary_key=True)
    warehousecompany_name = models.CharField(db_column='WarehouseCompany_Name', max_length=200)  # Field name made lowercase.
    warehouseaddress = models.CharField(db_column='WarehouseAddress', max_length=100)  # Field name made lowercase.
    warehousecity = models.CharField(db_column='WarehouseCity', max_length=30)  # Field name made lowercase.
    warehousegstin = models.CharField(db_column='WarehouseGSTIN', max_length=15)  # Field name made lowercase.
    warehousestate = models.CharField(db_column='WarehouseState', max_length=100)  # Field name made lowercase.
    warehousepincode = models.IntegerField(db_column='WarehousePincode')  # Field name made lowercase.
    warehousecontact = models.CharField(db_column='WarehouseContact', max_length=30)  # Field name made lowercase.
    warehouseemail = models.CharField(db_column='WarehouseEmail', max_length=100)  # Field name made lowercase.
    warehousetype = models.CharField(db_column='WarehouseType', max_length=100)  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    document = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registration_warehouse'


class TransportDriver(models.Model):
    id = models.BigAutoField(primary_key=True)
    driver_name = models.CharField(db_column='Driver_Name', max_length=100)  # Field name made lowercase.
    driver_contact = models.CharField(db_column='Driver_Contact', max_length=20)  # Field name made lowercase.
    driver_email = models.CharField(db_column='Driver_Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vehicle_number = models.CharField(db_column='Vehicle_Number', max_length=100, blank=True, null=True)  # Field name made lowercase.
    transporter = models.ForeignKey('TransportTransporter', models.DO_NOTHING, db_column='Transporter_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transport_driver'


class TransportDriverLocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    driver = models.ForeignKey(TransportDriver, models.DO_NOTHING, db_column='Driver_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transport_driver_location'


class TransportTransporter(models.Model):
    id = models.BigAutoField(primary_key=True)
    transportername = models.CharField(db_column='TransporterName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    transporteraddress = models.CharField(db_column='TransporterAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    transporter_contact = models.CharField(db_column='Transporter_Contact', max_length=30)  # Field name made lowercase.
    transporter_email = models.CharField(db_column='Transporter_Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    warehouse = models.ForeignKey(RegistrationWarehouse, models.DO_NOTHING, db_column='Warehouse_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transport_transporter'
