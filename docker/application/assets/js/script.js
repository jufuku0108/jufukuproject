window.addEventListener('load', function(){
  const spn = document.getElementById("spn");

  const btn = document.getElementById("btn");
  if(btn != null){
    btn.addEventListener('click', function(){
      spn.style.visibility = "visible"
    },false)  
  }

  const linkElements = document.links;
  for(let i = 0; i < linkElements.length; i++){
    linkElements[i].addEventListener('click', function(){
      spn.style.visibility = "visible"
    },false)
  }

  const options = document.getElementById("page_item_numbers").options;
  for(let i = 0; i < options.length; i++){
    options[i].addEventListener('click', function(){
      spn.style.visibility = "visible"
    },false)
  }

  spn.style.visibility = "hidden";

  var pageSize = location.search.split('pageSize=')[1] ? location.search.split('pageSize=')[1] : '10';
  const op10 = document.getElementById("op10");
  const op20 = document.getElementById("op20");
  const op30 = document.getElementById("op30");

  if (pageSize == "20"){
    op20.setAttribute('selected', true)

  } else if (pageSize == "30"){
    op30.setAttribute('selected', true)

  } else {
    op10.setAttribute('selected', true)

  }


}, false);

function togglerow(elm){
  var elm = document.getElementById(elm);
  if(elm.style.visibility == "collapse"){
    elm.style.visibility = "visible";
  }
  else
  {
    elm.style.visibility = "collapse";        
  }
}

function changeItemNumbers(url){
  const spn = document.getElementById("spn");
  spn.style.visibility = "visible";
  window.location.href=url;
}