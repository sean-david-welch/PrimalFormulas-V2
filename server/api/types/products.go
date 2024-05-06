package types

import (
	"github.com/google/uuid"
	"time"
)

type Product struct {
	ID          string  `json:"id"`
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Image       string  `json:"image"`
	Price       float32 `json:"price"`
	Created     string  `json:"created"`
}

func NewProduct(name, description, image string, price float32) *Product {
	return &Product{
		ID:          uuid.New().String(),
		Name:        name,
		Description: description,
		Image:       image,
		Price:       price,
		Created:     time.Now().UTC().Format(time.RFC3339),
	}
}
