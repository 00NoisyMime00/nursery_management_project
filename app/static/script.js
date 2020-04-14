var nursery = 'any';
var order = '';
var assigned = '';

function modalRole(role){
    nursery = role;
}

function modalOrder(ord){
    order = ord;
}

function modalAssigned(status){
    assigned = status;
}

function modalSaved(){
    console.log(nursery);
    window.location.href = '/view_employees?role='+nursery+'&order='+order+'&status='+assigned;
}
