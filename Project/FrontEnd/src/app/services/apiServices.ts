import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';


@Injectable()
export class apiServices {

    constructor(private httpClient: HttpClient) { }

    public pingAPI() {
        return this.httpClient.post(`${webServer}/ping`, null, { responseType: 'json' });
    }

    public endpointAPI() {
        return this.httpClient.post(`${webServer}/endpoint`, {"a":"b"}, { responseType: 'text' });
    }

    public loginAPI(user: String, pass: String) {
        return this.httpClient.post(`${webServer}/login`, {"user":user, "pass":pass}, { responseType: 'text' });
    }

    public logoutAPI(){
        return this.httpClient.post(`${webServer}/logout`, { responseType: 'text' });
    }
    
    public checkPrivateData(){
        return this.httpClient.post(`${webServer}/check_privatedata`, null, { responseType: 'text' });
    }

    public newPrivateData(uniqueKey: String){
        return this.httpClient.post(`${webServer}/add_pubkey`, {'encryptionKey':uniqueKey}, { responseType: 'text' });
    }

}