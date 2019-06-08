import { Component, OnInit, DoCheck } from '@angular/core';
import { apiServices } from '../services/apiServices';
import { componentState } from '../services/componentService';
import { FormControl } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { MarkdownService } from 'ngx-markdown';
@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit {

  toggleModal: String = "block";

  message = new FormControl('');
  loading: boolean = false;

  messageLoading: boolean = true;
  messageList: any;

  notify: boolean;

  isSearching = false;
  searchList = [];
  searchZero = false;
  searched: string;
  
  showMarked = false;
  modalMarked = 'none';
  public markedDownMessage: string;
  

  constructor(private API: apiServices, private state: componentState, private markService: MarkdownService) {

  }

  ngOnInit() {
    this.fetchPublicMessages();
    this.state.session.subscribe(
      () => {
        if (Boolean(sessionStorage.getItem('inSession'))) {
          this.toggleModal = 'none';
        }
      });
    setInterval(()=>{
      this.fetchPublicMessages();
    },30000)

    this.state.searchTrigger.subscribe((search)=>{
      if(search != '' || search != null){
        this.searchList = [];
        this.isSearching = true;
        this.searchZero = false;
        for (let index = 0; index < this.messageList.length; index++) {
          // this.searchList = this.messageList[index][0];
          if (this.messageList[index][0].substring(0, search.length) == search){
            this.searchList.push(this.messageList[index]);
          }
        }
        if(this.searchList.length == 0){
          this.searchZero = true;
          this.searched = search;
        }
      }
      else{
        this.searchList = [];
        this.searchZero = false;
        this.isSearching = false;
      }
    });
    this.notify = !Boolean(sessionStorage.getItem('inSession'));

  }

  showMarkDown(message:string){
    this.showMarked = true;
    this.modalMarked = 'block';
    
    // this.markedDownMessage = this.markService.compile(message);
    this.markedDownMessage = message
    // console.log(message)
    // console.log(this.markedDownMessage)
    

  }

  closeMarkDown(){
    this.showMarked = false;
    this.modalMarked = 'none';
    this.markedDownMessage = null;
  }

  onKeydown(event) {
    if (!this.loading){
      this.sendMessage();
    }
  }

  sendMessage() {
    this.API.broadcast(this.message.value);
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
      this.message.patchValue(null);
      this.fetchPublicMessages();
    }, 2000);
  }

  fetchPublicMessages() {
    this.API.get_broadcastMessages().then(
      (response) => {
        console.log(response);
        for (let index = 0; index < response.length; index++) {
          response[index][2] = response[index][2]*1000;          
        }
        this.messageList = response;
        this.messageLoading = false;
      }
    );
  }

}
