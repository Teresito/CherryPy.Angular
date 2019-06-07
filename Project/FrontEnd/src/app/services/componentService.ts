import { Subject } from 'rxjs';
import { Injectable, Injector } from '@angular/core';
import { Router } from '@angular/router';
import { apiServices } from './apiServices';

@Injectable()
export class componentState {
    notified = true;
    onlineUsers: any;

    clientState = new Subject<any>();
    session = new Subject<any>();



    constructor(private route: Router){}

    setClient(username: string, bool: boolean){
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('authenticated', bool.toString());
        this.route.navigate(['/broadcast'])
        this.clientState.next();
    }

    clearClient(){
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('authenticated');
        this.route.navigate(['/login'])
        this.clientState.next();
    }

    getUser(){
        sessionStorage.getItem('username');
    }

    getAuth(){
        return Boolean(sessionStorage.getItem('authenticated'));
    }
    
    setABadAccess(bool: boolean){
        sessionStorage.setItem('badAccess', bool.toString());
    }

    getBadAccess(){
        return Boolean(sessionStorage.getItem('badAccess'));
    }

}