const orderForm = document.getElementById("orderForm");
orderForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = {
    receiverCompanyName: document.getElementById("receiverCompanyName").value,
    receiverCompanyAddress: document.getElementById("receiverCompanyAddress")
      .value,
    receiverCompanyGSTIN: document.getElementById("receiverCompanyGSTIN").value,
    receiverCompanyContact: document.getElementById("receiverCompanyContact")
      .value,
    receiverCompanyEmail: document.getElementById("receiverCompanyEmail").value,
    receiverCompanyState: document.getElementById("receiverCompanyState").value,
    receiverCompanyCity: document.getElementById("receiverCompanyCity").value,
    TransporterName: document.getElementById("transporter").value,
    modeOfTransport: document.getElementById("modeOfTransport").value,
    vehicleNumber: document.getElementById("vehicleNumber").value,
    reasonForTransport: document.getElementById("reasonForTransport").value,
    cewbNo: document.getElementById("cewbNo").value,
    multiVehInfo: document.getElementById("multiVehInfo").value,
    invoiceNumber: document.getElementById("invoiceNumber").value,
    valueOfGoods: document.getElementById("valueOfGood").value,
    ValidityBill: document.getElementById("Validity").value,
  };

  if (!confirm("You sure?")) {
    return;
  }

  const response = await fetch("http://127.0.0.1:8000/outbound/submit_Form", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  console.log(response);
  const result = await response.json();
});

//fetching data from database and adding it into the tableOut

const fetchBillData = async function(){
  const response = await fetch("http://127.0.0.1:8000/outbound/get-inventory-data",{
    method:"GET",
    headers:{
      'Content-Type':'application/json',
    }
  });

  const data = await response.json();
  console.log(data)
  if(!response.ok){
    throw new Error(`HTTP error! Status : ${response.status}`);
  }
  else{
    updateTable(data.data,data.receiver);
  }
}

// document.addEventListener("DOMContentLoaded", fetchBillData);
setTimeout(fetchBillData, 1000);
