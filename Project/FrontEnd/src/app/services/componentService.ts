import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { apiServices } from './apiServices';
import { Router } from '@angular/router';

@Injectable()
export class componentState {

    constructor(private API: apiServices){}

    inSession = false;
    
    session = new Subject<any>();
    loggedChanged = new Subject<any>();
    usersUpdated = new Subject<any>();

    reportTimer: any;
    usersTimer: any;
    onlineUsers: any;

    setLoggedIn(bool: boolean){
        sessionStorage.setItem('loggedIn', String(bool));
    }

    getLoggedIn(){
        return Boolean(sessionStorage.getItem('loggedIn'));
    }

    deleteSession(){
        sessionStorage.clear();
    }
    
    setNotify(bool: boolean){
        sessionStorage.setItem('notified', String(bool));
    }

    getNotify(){
        return Boolean(sessionStorage.getItem('notified'));
    }

    logout(){
        this.API.logoutAPI().subscribe(
            (response) => {
                this.setLoggedIn(false);
                this.startSession(false);
                this.deleteSession();
                this.setNotify(true)
                this.loggedChanged.next();
                clearInterval(this.reportTimer);
                clearInterval(this.usersTimer);
            }
        );
    }

    startSession(session:boolean){
        this.inSession = session;
        if(session){
            // Call once
            this.reportUser();
            this.updateUsers();
            // Call intervally
            this.reportTimer = setInterval( ()=>{this.reportUser()}, 10000); // 10 Seconds
            this.usersTimer = setInterval(() => { this.updateUsers()}, 30000); // 1 minute
            this.setNotify(false);
        }
        else{
            clearInterval(this.reportTimer);
            clearInterval(this.usersTimer);
        }
    }


    private reportUser(){
        this.API.reportUser().subscribe((response) => {
            if (response == '2') {
                this.logout();
            }
        })
    }

    private updateUsers(){
        this.API.listUserAPI().subscribe((response) => {
            if (response == '2') {
                this.logout();
           }
           else{
               this.onlineUsers = response['userList'];
               this.usersUpdated.next();
           }
        })
    }
}