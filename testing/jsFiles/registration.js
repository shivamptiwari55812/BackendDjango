
document.getElementById("setWarehouseForm").addEventListener("submit", async function(event){
    event.preventDefault();

    const setWarehouseData ={
        warehouseName:document.getElementById("WarehouseCompany_Name").value,
        warehouseCity : document.getElementById("WarehouseCompany_City").value,
        warehouseEmail : document.getElementById("WarehouseCompany_Email").value,
        warehouseContact : document.getElementById("WarehouseCompany_Contact").value,
        warehouseAddress : document.getElementById("WarehouseCompany_Address").value,
        warehouseState : document.getElementById("WarehouseCompany_State").value,
        warehouseGSTIN : document.getElementById("WarehouseCompany_GSTIN").value,
        warehouseCapacity : document.getElementById("WarehouseCompany_Capacity").value,
        TypeOfWarehouse : document.getElementById("TypeOfWarehouse").value,
        warehousePincode : document.getElementById("WarehouseCompany_Pincode").value,
        warehouseAvailable : document.getElementById("WarehouseStatus").value
    }

    
    const response = await fetch('http://127.0.0.1:8000/app1/submit_Warehouseform',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(setWarehouseData),
    });

    const result = await response.json();
    // alert(result.message);
})