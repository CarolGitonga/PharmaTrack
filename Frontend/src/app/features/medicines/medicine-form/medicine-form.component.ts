import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MedicineService } from '../../../core/services/medicine.service';

@Component({
  selector: 'app-medicine-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatIconModule,
    MatCardModule,
  ],
  templateUrl: './medicine-form.component.html',
  styleUrl: './medicine-form.component.scss'
})
export class MedicineFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private medicineService = inject(MedicineService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private snackBar = inject(MatSnackBar);

  isEditMode = false;
  medicineId: number | null = null;
  loading = false;
  saving = false;

  categories = ['Antibiotic', 'Antimalarial', 'Painkiller', 'Antifungal', 'Vitamin', 'Antiviral', 'Other'];
  units = ['pcs', 'strips', 'bottles', 'sachets', 'vials', 'tubes'];

  form = this.fb.group({
    name: ['', Validators.required],
    generic_name: [''],
    category: ['', Validators.required],
    manufacturer: [''],
    batch_number: [''],
    quantity: [0, [Validators.required, Validators.min(0)]],
    minimum_quantity: [10, [Validators.required, Validators.min(1)]],
    buying_price: [null, [Validators.required, Validators.min(0)]],
    selling_price: [null, [Validators.required, Validators.min(0)]],
    expiry_date: [null, Validators.required],
    supplier: [''],
    unit: ['pcs', Validators.required],
  });

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.medicineId = +id;
      this.loading = true;
      this.medicineService.getById(this.medicineId).subscribe({
        next: (m) => {
          this.form.patchValue({
            ...m as any,
            expiry_date: new Date(m.expiry_date) as any,
          });
          this.loading = false;
        },
        error: () => {
          this.snackBar.open('Failed to load medicine.', 'Close', { duration: 3000 });
          this.router.navigate(['/medicines']);
        }
      });
    }
  }

  submit(): void {
    if (this.form.invalid) return;

    this.saving = true;
    const value = this.form.value;
    const expiryDate = value.expiry_date as unknown as Date;
    const payload: any = {
      ...value,
      expiry_date: expiryDate instanceof Date
        ? expiryDate.toISOString().split('T')[0]
        : value.expiry_date,
    };

    const request = this.isEditMode
      ? this.medicineService.update(this.medicineId!, payload)
      : this.medicineService.create(payload);

    request.subscribe({
      next: () => {
        this.snackBar.open(
          `Medicine ${this.isEditMode ? 'updated' : 'added'} successfully.`,
          'Close', { duration: 3000 }
        );
        this.router.navigate(['/medicines']);
      },
      error: () => {
        this.snackBar.open('Failed to save medicine.', 'Close', { duration: 3000 });
        this.saving = false;
      }
    });
  }
}
