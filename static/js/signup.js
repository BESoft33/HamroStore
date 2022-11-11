function validatePassword(){
  const password = document.getElementById("first_pass").value;
  const c_password = document.getElementById("second_pass").value;
  if (password !== c_password){
    alert("password do not match");
    return false;
  }else {
  return true;
  }
}
