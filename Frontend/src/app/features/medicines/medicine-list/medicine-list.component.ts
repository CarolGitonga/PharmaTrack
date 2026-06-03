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
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MedicineService, Medicine } from '../../../core/services/medicine.service';
import { ConfirmDialogComponent } from '../../../shared/confirm-dialog/confirm-dialog.component';

type Tab = 'all' | 'low-stock' | 'expiring' | 'expired';

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
    MatDialogModule,
    ConfirmDialogComponent,
  ],
  templateUrl: './medicine-list.component.html',
  styleUrl: './medicine-list.component.scss',
})
export class MedicineListComponent implements OnInit {
  private medicineService = inject(MedicineService);
  private snackBar = inject(MatSnackBar);
  private dialog = inject(MatDialog);

  @ViewChild(MatSort) sort!: MatSort;

  displayedColumns = ['name', 'category', 'quantity', 'expiry_date', 'status', 'actions'];
  dataSource = new MatTableDataSource<Medicine>();
  loading = true;
  searchQuery = '';
  lastLoaded: Date | null = null;
  activeTab: Tab = 'all';

  private allMedicines: Medicine[] = [];

  get counts() {
    return {
      all:       this.allMedicines.length,
      lowStock:  this.allMedicines.filter(m => m.is_low_stock).length,
      expiring:  this.allMedicines.filter(m => m.is_expiring_soon).length,
      expired:   this.allMedicines.filter(m => m.is_expired).length,
    };
  }

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
        this.allMedicines = data;
        this.lastLoaded = new Date();
        this.dataSource.filterPredicate = (medicine, filter) => {
          const search = filter.toLowerCase();
          return medicine.name.toLowerCase().includes(search) ||
                 medicine.category.toLowerCase().includes(search);
        };
        this.applyTab(this.activeTab);
        this.loading = false;
      },
      error: () => {
        this.snackBar.open('Failed to load medicines.', 'Close', { duration: 3000 });
        this.loading = false;
      },
    });
  }

  selectTab(tab: Tab): void {
    this.activeTab = tab;
    this.searchQuery = '';
    this.applyTab(tab);
  }

  private applyTab(tab: Tab): void {
    switch (tab) {
      case 'low-stock': this.dataSource.data = this.allMedicines.filter(m => m.is_low_stock);   break;
      case 'expiring':  this.dataSource.data = this.allMedicines.filter(m => m.is_expiring_soon); break;
      case 'expired':   this.dataSource.data = this.allMedicines.filter(m => m.is_expired);      break;
      default:          this.dataSource.data = this.allMedicines;
    }
  }

  applyFilter(): void {
    this.dataSource.filter = this.searchQuery.trim().toLowerCase();
  }

  getStatus(medicine: Medicine): string {
    if (medicine.is_expired) return 'expired';
    if (medicine.quantity === 0) return 'out-of-stock';
    if (medicine.is_low_stock) return 'low-stock';
    return 'in-stock';
  }

  getStatusLabel(medicine: Medicine): string {
    if (medicine.is_expired) return 'Expired';
    if (medicine.quantity === 0) return 'Out of Stock';
    if (medicine.is_low_stock) return 'Low Stock';
    return 'In Stock';
  }

  delete(medicine: Medicine): void {
    const ref = this.dialog.open(ConfirmDialogComponent, {
      width: '400px',
      data: {
        title: 'Deactivate Medicine',
        message: `Are you sure you want to deactivate ${medicine.name}? It will be removed from your active inventory.`,
        confirmText: 'Deactivate',
      },
    });

    ref.afterClosed().subscribe(confirmed => {
      if (!confirmed) return;
      this.medicineService.delete(medicine.id).subscribe({
        next: () => {
          this.snackBar.open(`${medicine.name} deactivated.`, 'Close', { duration: 3000 });
          this.loadMedicines();
        },
        error: () => this.snackBar.open('Failed to deactivate.', 'Close', { duration: 3000 }),
      });
    });
  }
}
