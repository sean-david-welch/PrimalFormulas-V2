import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetFormComponent } from './asset-form.component';

describe('AssetFormComponent', () => {
  let component: AssetFormComponent;
  let fixture: ComponentFixture<AssetFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssetFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AssetFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
