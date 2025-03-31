console.log("Shivam it is working")

//Adding product

const productForm = document.getElementById("productForm")
const transactionType = document.querySelector('input[name="TransactionType"]:checked');
productForm.addEventListener("submit", async function(){
    event.preventDefault();
    console.log("It is here")
    const formData ={
        productName : document.getElementById("productName").value,
        productQuantity : document.getElementById("quantity").value,
        productPrice : document.getElementById("price").value,
        productCategory : document.getElementById("category").value,
        transactionType : document.getElementById("TransactionType").value,
        ProductRejected : document.getElementById("productRejected").value
    }

    if(!confirm("You sure ?")){
        return 
    }

    const response = await fetch("http://127.0.0.1:8000/app1/add_item",{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(formData)
    });

    console.log(response)

    window.location.href="tableforInv.html";

})


//Displaying data on the Table
const getProductDetails = async function(){
    const response = await fetch ('http://127.0.0.1:8000/app1/get_product',{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
        }
    });
    const data = await response.json();
    if(!response.ok){
        throw new Error(`HTTP error! Status : ${response.status}`);
    }
 
    else
    {
        displayDatatable(data.data);
        displayStatustable(data.data);
    }
    console.log(data)
}

function redirectToEditPage(productId) {
    if(!confirm("You will be redirected to another page!")){
        return
    }
    const storageId= localStorage.setItem('productId', productId);
    console.log(storageId)
    window.location.href = `inventoryEdit.html?id=${productId}`;
}



const displayDatatable = async function(data){
    const tableBody = document.getElementById('tablebody');
    tableBody.innerHTML ='';
    data.forEach((item) => { 
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.ProductName}</td>
            <td>${item.ProductQuantity}</td>
            <td>${item.ProductPrice}</td>
            <td>${item.ProductCategory}</td>
            <td>${item.Transaction_type}</td>
            <td>${item.Product_Rejected}</td>
             <td>
                <button class="edit-btn" onclick="redirectToEditPage(${item.id})">Edit</button>
                <button class="delete-btn" onclick="deleteProduct(${item.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });

}
setTimeout(getProductDetails,1000);


//Editing the product

const editProduct = async function(id){



    const response = await fetch('http://127.0.0.1:8000/app1/edit_product',{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify({id})
    });

    const data = await response.json();
}


//product status 
// const get_product_Status = async function(){

//     try{
//     console.log("Shivam")
//     const response = await fetch('http://127.0.0.1:8000/app1/get_product_status',{
//         method:'GET',
//         headers:{
//             'Content-Type':'application/json',
//         }
//     });
//     const data = await response.json();
//     console.log(data)
//     if(!response.ok){
//         throw new Error(`HTTP error! Status : ${response.status}`);
//     }

//     else{
//         displayStatustable(data.data);
//     }
// }
// catch(error){
//     console.error(error);
// }
    
// }

const displayStatustable= async function(data){
    console.log("Shivam")
    const table2Body = document.getElementById('stockTableBody');
    table2Body.innerHTML ='';
    data.forEach((item)=>{
        let row = document.createElement("tr");
        row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.ProductName}</td>
        <td>${item.ProductQuantity}</td>
        <td>${item.status}</td>
        `
        table2Body.appendChild(row);
    }

    )}
    


    const productid = localStorage.getItem('productId');

    if(!productid){
        alert("No item was selected for the edit");
        window.location.href="tableforInv.html";
        
        

    }

    fetch(`http://127.0.0.1:8000/app1/get_productDetails/${productid}`,{
        method:"GET",
        headers:{
            "content-type":"application/json"
        }
    })

    .then(response => response.json())
    
    .then(data => {
        console.log(response)
        document.getElementById("productName").value = data.ProductName;
        document.getElementById("price").value = data.ProductPrice;
        document.getElementById("quantity").value = data.ProductQuantity;
        document.getElementById("productRejected").value = data.Product_Rejected;
        document.getElementById("productRestock").value = data.ProductRestock;
        document.getElementById("category").value = data.ProductCategory;
        document.querySelector(`input[name="TransactionType"][value="${data.Transaction_type}"]`).checked = true;
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });
    