# Database Project Description: Pet Sitting Service Platform

This database project aims to create a pet sitting service platform that connects pet owners with professional pet sitters. The platform allows pet owners to find suitable pet sitters for their pets and make job offers to them. The pet sitters can accept or decline the job offers based on their availability and preferences. After completing the job, both pet owners and pet sitters can rate each other based on their experience.

# The database consists of the following tables:

**portfolio:** This table stores information about pet sitters registered on the platform. It includes fields such as username (primary key), email, phone number, years of experience, and password. The table enforces constraints on the phone number length and password length.

**pet: **This table stores information about pets owned by pet owners. It includes fields such as pet name, pet ID (primary key), type, breed, and the username of the pet owner (references portfolio table). Each pet belongs to a specific pet owner.

**joboffer:** This table stores information about job offers made by pet owners to pet sitters. It includes fields such as offer ID (primary key), price, location, start date, end date, and the pet ID (references pet table). The table enforces constraints to ensure that the start date is before the end date, and each job offer is unique based on the start date, end date, and pet ID.

**pending:** This table stores information about pending job offers that pet sitters need to respond to. It includes fields such as offer ID (references joboffer table) and the pet sitter's username (references portfolio table). The table enforces constraints to ensure that each job offer and pet sitter combination is unique.

**transaction: **This table stores information about completed job offers. It includes fields such as offer ID (references joboffer table) and the pet sitter's username (references portfolio table). Each entry represents a successful transaction between a pet owner and a pet sitter.

**to_rate:** This table stores information about job offers that need to be rated. It includes fields such as offer ID (references joboffer table) and a rating given by the pet owner (between 0 and 5). The table enforces constraints on the rating value.

This database schema efficiently manages job offers, pending requests, completed transactions, and ratings within the pet sitting service platform. It provides the necessary structure to handle interactions between pet owners and pet sitters, ensuring the smooth operation of the platform.
