package models

import (
	"github.com/google/uuid"
	"time"
)

type About struct {
	ID          string `json:"id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Image       string `json:"image"`
	Created     string `json:"created"`
}

func NewAbout(title, description, image string) *About {
	return &About{
		ID:          uuid.New().String(),
		Title:       title,
		Description: description,
		Image:       image,
		Created:     time.Now().UTC().Format(time.RFC3339),
	}
}
