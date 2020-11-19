import { Component, OnInit } from '@angular/core';
import * as mqtt from 'mqtt';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  client = mqtt.connect("mqtt://192.168.1.6");
  messages = []
  constructor() { }

  ngOnInit(): void {
    this.client.subscribe('test_channel', (err) => {
      if(!err){
        this.client.publish('esp/data', 'hello i am rasp');
      }
    })
    this.client.on('message', (topic, message)=> {
      this.messages.push("topic: " + topic + "message: " + message);
    })
  }

}
