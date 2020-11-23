// API END POINTS
WEB_APP_IP="127.0.0.1"
WEB_APP_PORT="8884"
const ADV_ENDPOINT = `http://${WEB_APP_IP}:${WEB_APP_PORT}/advertisements`
const OPEN_ENDPOINT = `http://${WEB_APP_IP}:${WEB_APP_PORT}/command/open`


function add(sons) {
  console.log("adding ")
  let item = document.createElement('li')
  // item.innerHTML = msg
  // document.getElementById("list").appendChild(item)
  console.log('sons', sons);
  
  // OBSOLETE
  // $('#list').html('');
  // $.each(sons , (key,val)=> {$('#list').append("<li>"+"Topic: "+val.topic + " Payload: " + val.payload+"</li>"); console.log(val); console.log("topic", val.topic)})
  $('#tab_body').html('');
  $.each(sons , (key,val)=> {
    $('#tab_body').append( 
      "<tr>"+ "<td>"+val.topic+"</td>" + "<td>"+val.payload+"</td>"+"</tr>");
      console.log(val); console.log("topic", val.topic)
    }
    )
  
  // for (son in sons ){
  //   console.log(son)
  //   console.log("topic",son.topic)
  //   console.log("load", son.payload)
  // }
}

function get_amessage() {
  $.ajax({
      type: 'GET',
      url: ADV_ENDPOINT,
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
  let api = ADV_ENDPOINT
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

function openLock(btn) {
  let id = btn.getAttribute('id');
  console.log(`got btn id ${id}`);
  $.ajax({
    type: 'GET',
    url: OPEN_ENDPOINT+"?id="+id,
    // data: {get_param: 'value'},
    dataType: 'json',
    success: function (data) {
      var names = data
      console.log(data)
      // $('#list').html(data);
      // $.each(data, (key, val) => {console.log("key", key, "val", val); add(val)})
    }
  });
}

// windown.setInterval(()=> {
//   get_amessages()
// }, 2)