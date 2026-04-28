import { Routes } from '@angular/router';
import { authGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
  },
  {
    path: 'medicines',
    canActivate: [authGuard],
    loadComponent: () => import('./features/medicines/medicine-list/medicine-list.component').then(m => m.MedicineListComponent),
  },
  {
    path: 'medicines/add',
    canActivate: [authGuard],
    loadComponent: () => import('./features/medicines/medicine-form/medicine-form.component').then(m => m.MedicineFormComponent),
  },
  {
    path: 'medicines/edit/:id',
    canActivate: [authGuard],
    loadComponent: () => import('./features/medicines/medicine-form/medicine-form.component').then(m => m.MedicineFormComponent),
  },
  { path: '**', redirectTo: 'dashboard' },
];
