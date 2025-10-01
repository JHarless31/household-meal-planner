# Meal Planning App - Frontend

A modern, responsive web application for household meal planning, recipe management, and kitchen inventory tracking built with Next.js 14, React, TypeScript, and Tailwind CSS.

## Features

- **User Authentication**: Secure login and registration with JWT-based sessions
- **Recipe Management**: Create, edit, search, and rate recipes with versioning support
- **Inventory Tracking**: Monitor kitchen inventory with low stock and expiration alerts
- **Menu Planning**: Drag-and-drop weekly meal planning with automatic shopping lists
- **Shopping Lists**: Generate and manage shopping lists from menu plans
- **Ratings & Feedback**: Rate recipes with thumbs up/down and track household favorites
- **Admin Portal**: User management and application settings (admin-only)
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop devices
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **Data Fetching**: Axios with TanStack Query
- **Drag & Drop**: @dnd-kit
- **Form Handling**: React Hook Form
- **Date Utilities**: date-fns
- **Testing**: Jest + React Testing Library

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000` (or configured via environment variables)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd /path/to/menu_app/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_API_BASE_PATH=/api
   ```

## Development

Start the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Building for Production

```bash
npm run build
npm run start
# or
yarn build
yarn start
```

## Testing

Run tests:

```bash
npm run test
# or
yarn test
```

Run tests in watch mode:

```bash
npm run test:watch
# or
yarn test:watch
```

Generate coverage report:

```bash
npm run test:coverage
# or
yarn test:coverage
```

## Code Quality

### Linting

```bash
npm run lint
# or
yarn lint
```

### Type Checking

```bash
npm run type-check
# or
yarn type-check
```

### Formatting (with Prettier - configured)

Prettier is configured in `.prettierrc`. Most IDEs can auto-format on save.

## Project Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── (main)/              # Authenticated app pages
│   │   │   ├── page.tsx         # Dashboard
│   │   │   ├── recipes/         # Recipe pages
│   │   │   ├── inventory/       # Inventory pages
│   │   │   ├── menu-plans/      # Menu planning pages
│   │   │   └── admin/           # Admin pages
│   │   ├── auth/                # Authentication pages
│   │   └── layout.tsx           # Root layout
│   ├── components/              # React components
│   │   ├── common/              # Reusable UI components
│   │   ├── layout/              # Layout components
│   │   ├── recipes/             # Recipe-specific components
│   │   ├── ratings/             # Rating components
│   │   └── ...
│   ├── contexts/                # React contexts
│   │   ├── AuthContext.tsx      # Authentication state
│   │   └── ToastContext.tsx     # Toast notifications
│   ├── lib/                     # Libraries and utilities
│   │   ├── api/                 # API client modules
│   │   ├── types/               # TypeScript type definitions
│   │   └── utils/               # Utility functions
│   └── styles/                  # Global styles
├── public/                      # Static assets
├── tests/                       # E2E tests (Playwright)
├── .env.example                 # Environment variables template
├── next.config.js               # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies and scripts
```

## Key Components

### Authentication
- **AuthContext**: Manages user authentication state
- **ProtectedRoute**: Wrapper for authenticated routes
- **Login/Register**: Authentication forms

### Recipes
- **RecipeCard**: Recipe summary display
- **RecipeForm**: Create/edit recipe form
- **RatingWidget**: Thumbs up/down rating interface

### Common Components
- **Button**: Reusable button with variants
- **Input/Select/Textarea**: Form inputs with validation
- **Modal**: Accessible modal dialogs
- **Toast**: Notification system
- **LoadingSpinner**: Loading states
- **ErrorMessage**: Error handling UI

## API Integration

The frontend communicates with the backend API using axios. All API calls are centralized in `src/lib/api/`:

- `auth.ts` - Authentication endpoints
- `recipes.ts` - Recipe CRUD operations
- `inventory.ts` - Inventory management
- `menuPlans.ts` - Menu planning
- `ratings.ts` - Recipe ratings
- `shoppingLists.ts` - Shopping list generation
- `admin.ts` - Admin operations

### Authentication Flow

The app uses JWT cookies for authentication:

1. User logs in via `/auth/login`
2. Backend sets HttpOnly cookie with JWT
3. All subsequent requests include cookie automatically
4. AuthContext manages user state
5. ProtectedRoute wrapper ensures authentication

## Accessibility

The app follows WCAG 2.1 Level AA guidelines:

- Semantic HTML elements
- ARIA labels and roles
- Keyboard navigation support
- Focus management
- Sufficient color contrast
- Screen reader compatibility
- Alt text for images

## Responsive Design

Mobile-first approach with breakpoints:

- Mobile: 320px+
- Tablet: 768px+
- Desktop: 1024px+
- Large: 1280px+

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

## Deployment

### Docker Deployment

A `Dockerfile` is provided for containerized deployment:

```bash
docker build -t meal-planning-frontend .
docker run -p 3000:3000 meal-planning-frontend
```

### Environment Variables for Production

Ensure the following are set in production:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_API_BASE_PATH=/api
```

## Troubleshooting

### API Connection Issues

If you encounter CORS errors or connection issues:

1. Verify backend is running on the correct port
2. Check `NEXT_PUBLIC_API_URL` in `.env`
3. Ensure backend CORS settings allow frontend origin

### Build Errors

If build fails:

1. Delete `node_modules` and `.next` folders
2. Run `npm install` again
3. Run `npm run build`

### TypeScript Errors

Run type checking separately:

```bash
npm run type-check
```

## Contributing

1. Follow the existing code style (Prettier/ESLint configured)
2. Write tests for new features
3. Ensure all tests pass before submitting
4. Update documentation as needed

## License

This project is part of the Household Meal Planning System.

## Support

For issues or questions:

- Check documentation in `docs/` folder
- Review API specification in `docs/API_SPEC.yaml`
- Open an issue in the repository
