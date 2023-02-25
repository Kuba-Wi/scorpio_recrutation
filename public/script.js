// var $container = $("#cont");
// var $itens = $( ".item" )
// // $itens.append("<div class='left'>move left</div><div class='right'>move right</div>");


// $container.packery();
// $itens.draggable({
//       stop: function() {
//         window.setTimeout(function() {$container.packery()}, 100);
//       }
//     });
// $itens.click(function() {
//     $(this).hide();
// })
// $container.packery('bindUIDraggableEvents', $itens);

// function orderItems() {
//   var result = "";
//   $($container.packery('getItemElements')).each( function(i, el) {
//     result += i+1 + "-" + $(el).text() + "<br>";
//   });
// //   $("#result").html(result);
// }

// $container.packery( 'on', 'layoutComplete', orderItems );
// $container.packery( 'on', 'dragItemPositioned', orderItems );


// const fs = require("fs");
// fs.readFile("system_data_readings.txt", (err, data) => {
//   if (err) throw err;

//   console.log(data.toString());
// });

const ram_total = document.getElementById("ram_total")
const ram_used = document.getElementById("ram_used")
const ram_avail = document.getElementById("ram_avail")
const disk_free = document.getElementById("disk_free")

const cpu_table = document.getElementById("cpu_table")
const network_table = document.getElementById("network_table")
const ram_table = document.getElementById("ram_table")

async function download_system_readings() {
    const res_promise = await fetch("", {
        method: "POST"
    })
    var response = await res_promise.json()
    ram_total.innerText = response.RAM.total
    ram_used.innerText = response.RAM.used
    ram_avail.innerText = response.RAM.available
    disk_free.innerText = response.disk
    
    cpu_table.innerHTML = `<th colspan="2">CPU core usage [%]</th>`
    response.CPU.forEach((el, index) => {
        cpu_table.innerHTML += `<tr><td>CPU${index+1}</td><td>${el}</td></tr>`
    })
    
    cpu_table.innerHTML += `<th colspan="2">Sensors temperature &#8451;</th>`
    response.temp.forEach(el => {
        cpu_table.innerHTML += `<tr><td class="center-cell" colspan="2">${el}</td></tr>`
    })
    
    network_table.innerHTML = `<th colspan="2">Network interfaces</th>`
    for (const ifname in response.network) {
        network_table.innerHTML += `<th colspan="2">${ifname}</th>`
        network_table.innerHTML += `<tr><td>status</td><td>${response.network[ifname].status}</td></tr>`
        network_table.innerHTML += `<tr><td>ip</td><td>${response.network[ifname].ip}</td></tr>`
        network_table.innerHTML += `<tr><td>receive speed [b/s]</td><td>${response.network[ifname].recv_speed}</td></tr>`
        network_table.innerHTML += `<tr><td>send speed [b/s]</td><td>${response.network[ifname].send_speed}</td></tr>`
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

download_system_readings()

const ram_but = document.getElementById("ram_but")
ram_but.addEventListener("click", async () => {
    ram_table.style.visibility = (ram_table.style.visibility === "visible") ? "hidden" : "visible"
})

const cpu_but = document.getElementById("cpu_but")
cpu_but.addEventListener("click", () => {
    cpu_table.style.visibility = (cpu_table.style.visibility === "visible") ? "hidden" : "visible"
})

const network_but = document.getElementById("network_but")
network_but.addEventListener("click", () => {
    network_table.style.visibility = (network_table.style.visibility === "visible") ? "hidden" : "visible"
})

while (true) {
    await sleep(3000)
    download_system_readings()
}
