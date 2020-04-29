var nursery = 'any';
var order = '';
var assigned = '';

var pinn = '';
var cityy = '';
var countryy = '';

function modalRole(role){
    nursery = role;
}

function modalOrder(ord){
    order = ord;
}

function modalAssigned(status){
    assigned = status;
}

function modalPinCode(pin){
	pinn = pin;
}
function modalCity(city){
	cityy = city;
}

function modalCountry(country){
	countryy = country;
}

function modalSaved(){
    console.log(nursery);
    window.location.href = '/view_employees?role='+nursery+'&order='+order+'&status='+assigned;
}

function modalSaveNursery(){
	window.location.href = '/view_nurseries?pin='+pinn+'&city='+cityy+'&country='+countryy;
}
