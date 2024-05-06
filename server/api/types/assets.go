package types

import (
	"github.com/google/uuid"
	"time"
)

type Asset struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Content string `json:"content"`
	Created string `json:"created"`
}

func NewAsset(name, content string) *Asset {
	return &Asset{
		ID:      uuid.New().String(),
		Name:    name,
		Content: content,
		Created: time.Now().UTC().Format(time.RFC3339),
	}
}
