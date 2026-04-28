import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Medicine {
  id: number;
  name: string;
  generic_name: string;
  category: string;
  manufacturer: string;
  batch_number: string;
  quantity: number;
  minimum_quantity: number;
  buying_price: number;
  selling_price: number;
  expiry_date: string;
  supplier: string;
  unit: string;
  is_active: boolean;
  is_low_stock: boolean;
  is_expiring_soon: boolean;
  is_expired: boolean;
  days_to_expiry: number;
}

@Injectable({ providedIn: 'root' })
export class MedicineService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/medicines`;

  getAll(): Observable<Medicine[]> {
    return this.http.get<Medicine[]>(`${this.apiUrl}/`);
  }

  getById(id: number): Observable<Medicine> {
    return this.http.get<Medicine>(`${this.apiUrl}/${id}/`);
  }

  create(data: Partial<Medicine>): Observable<Medicine> {
    return this.http.post<Medicine>(`${this.apiUrl}/`, data);
  }

  update(id: number, data: Partial<Medicine>): Observable<Medicine> {
    return this.http.put<Medicine>(`${this.apiUrl}/${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}/`);
  }

  getLowStock(): Observable<Medicine[]> {
    return this.http.get<Medicine[]>(`${this.apiUrl}/low-stock/`);
  }

  getExpiring(): Observable<Medicine[]> {
    return this.http.get<Medicine[]>(`${this.apiUrl}/expiring/`);
  }

  getExpired(): Observable<Medicine[]> {
    return this.http.get<Medicine[]>(`${this.apiUrl}/expired/`);
  }
}
