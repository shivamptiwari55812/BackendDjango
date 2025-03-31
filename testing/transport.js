const TransporterForm = document.getElementById("setTransporterForm")
TransporterForm.addEventListener("submit",async function(){

  event.preventDefault();

  const setTransportData ={
    TransporterName : document.getElementById("Transporter").value,
    TransporterAddress : document.getElementById("TransporterAdd").value,
    TransporterContact : document.getElementById("TransporterContact").value,
    TransporterEmail : document.getElementById("TransporterEmail").value

  }

  const response = await fetch("http://127.0.0.1:8000/app1/setTransporter",{
    method: 'POST',
    headers:{
      'content-type':"application/json",
    },
    body:JSON.stringify(setTransportData),
  });

  const result = await response.json();
})

