function add(sons) {
  console.log("adding ")
  let item = document.createElement('li')
  // item.innerHTML = msg
  // document.getElementById("list").appendChild(item)
  console.log('sons', sons);
  $('#list').html('');
  $.each(sons , (key,val)=> {$('#list').append("<li>"+"topic: "+val.topic + " payload: " + val.payload+"</li>"); console.log(val); console.log("topic", val.topic)})
  // for (son in sons ){
  //   console.log(son)
  //   console.log("topic",son.topic)
  //   console.log("load", son.payload)
  // }
}

function get_amessage() {
  $.ajax({
      type: 'GET',
      url: 'http://127.0.0.1:5000/messages',
      // data: {get_param: 'value'},
      dataType: 'json',
      success: function (data) {
        var names = data
        console.log(data)
        // $('#list').html(data);
        add(data)
        // $.each(data, (key, val) => {console.log("key", key, "val", val); add(val)})
      }
    });
}
// vanilla failed to parse data
function get_messages(cb) {
  let api = "http://127.0.0.1:5000/messages"
  let xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = ()=> {
    if(xhttp.readyState === 4 && xhttp.status == 200){
      console.log("ready!!");
      let son = xhttp.json;
      console.log("raw",son)
      console.log("stringify", JSON.stringify(son));
      console.log("parse",JSON.parse(son))
      cb(son);
    } else {
      console.log("xelse ")
    }
    console.log("heak");
  }
  xhttp.open("GET", api, true)
  xhttp.send()
}
