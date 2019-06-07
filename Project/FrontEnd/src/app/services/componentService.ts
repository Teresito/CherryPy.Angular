import { Subject } from 'rxjs';
import { Injectable, Injector } from '@angular/core';
import { Router } from '@angular/router';
import { apiServices } from './apiServices';

@Injectable()
export class componentState {
    clientState = new Subject<any>();
    session = new Subject<any>();
    usersList: any;


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
        sessionStorage.removeItem('inSession');
        this.route.navigate(['/login'])
        this.clientState.next();
        this.session.next();
    }

    getAuth(){
        return Boolean(sessionStorage.getItem('authenticated'));
    }

}