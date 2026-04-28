import { Component, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MedicineService, Medicine } from '../../../core/services/medicine.service';

@Component({
  selector: 'app-medicine-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    MatTableModule,
    MatSortModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatTooltipModule,
  ],
  templateUrl: './medicine-list.component.html',
  styleUrl: './medicine-list.component.scss'
})
export class MedicineListComponent implements OnInit {
  private medicineService = inject(MedicineService);
  private snackBar = inject(MatSnackBar);

  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['name', 'category', 'quantity', 'expiry_date', 'status', 'actions'];
  dataSource = new MatTableDataSource<Medicine>();
  loading = true;
  searchQuery = '';

  ngOnInit(): void {
    this.loadMedicines();
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  loadMedicines(): void {
    this.loading = true;
    this.medicineService.getAll().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        this.dataSource.filterPredicate = (medicine, filter) => {
          const search = filter.toLowerCase();
          return medicine.name.toLowerCase().includes(search) ||
                 medicine.category.toLowerCase().includes(search);
        };
        this.loading = false;
      },
      error: () => {
        this.snackBar.open('Failed to load medicines.', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  applyFilter(): void {
    this.dataSource.filter = this.searchQuery.trim().toLowerCase();
  }

  getStatus(medicine: Medicine): string {
    if (medicine.is_expired) return 'expired';
    if (medicine.is_expiring_soon) return 'expiring';
    if (medicine.is_low_stock) return 'low-stock';
    return 'ok';
  }

  getStatusLabel(medicine: Medicine): string {
    if (medicine.is_expired) return 'Expired';
    if (medicine.is_expiring_soon) return 'Expiring Soon';
    if (medicine.is_low_stock) return 'Low Stock';
    return 'OK';
  }

  delete(medicine: Medicine): void {
    if (!confirm(`Deactivate ${medicine.name}?`)) return;
    this.medicineService.delete(medicine.id).subscribe({
      next: () => {
        this.snackBar.open(`${medicine.name} deactivated.`, 'Close', { duration: 3000 });
        this.loadMedicines();
      },
      error: () => this.snackBar.open('Failed to deactivate.', 'Close', { duration: 3000 })
    });
  }
}
