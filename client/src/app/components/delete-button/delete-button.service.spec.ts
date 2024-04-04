import { TestBed } from '@angular/core/testing';

import { DeleteButtonService } from './delete-button.service';

describe('DeleteButtonService', () => {
  let service: DeleteButtonService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DeleteButtonService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
