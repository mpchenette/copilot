# Monorepo Custom Instructions

## Repository Structure

This monorepo contains multiple applications and shared libraries organized under the following structure:

- `apps/` - Application projects
  - `web-dashboard/` - React-based admin dashboard
  - `mobile-app/` - React Native mobile application
  - `api-gateway/` - Node.js API gateway service
  - `worker-service/` - Background job processor
- `packages/` - Shared libraries and components
  - `ui-components/` - Reusable UI component library
  - `data-models/` - TypeScript type definitions and schemas
  - `utils/` - Common utility functions
  - `config/` - Shared configuration files
- `infrastructure/` - Infrastructure as Code
  - `terraform/` - Terraform modules
  - `kubernetes/` - K8s manifests and Helm charts
- `docs/` - Documentation
  - `architecture/` - System architecture diagrams
  - `api-specs/` - OpenAPI specifications
  - `runbooks/` - Operational procedures

## Code Standards and Practices

### General Principles

1. **Consistency Across Projects**: Maintain consistent coding styles, patterns, and conventions across all applications and packages in the monorepo.

2. **Shared Code Philosophy**: Before duplicating code, always consider if it belongs in a shared package under `packages/`.

3. **Dependency Management**: 
   - Use workspace protocol for internal dependencies (e.g., `"@acme/ui-components": "workspace:*"`)
   - Keep external dependencies synchronized across projects where possible
   - Document any intentional version discrepancies

4. **Incremental Changes**: When modifying shared packages, consider the impact on all consuming applications and update them accordingly.

### TypeScript Guidelines

- Use strict mode enabled in all `tsconfig.json` files
- Prefer interfaces over types for object shapes
- Use `unknown` instead of `any` when type is truly unknown
- Export types from `packages/data-models` for cross-project usage

### Testing Standards

- **Unit Tests**: Required for all business logic in `packages/` and `apps/*/src/services/`
- **Integration Tests**: Required for API endpoints and database interactions
- **E2E Tests**: Required for critical user flows in web and mobile apps
- **Coverage Threshold**: Maintain minimum 80% code coverage for shared packages

### Architecture Patterns

#### Shared Package Development

When creating or modifying packages under `packages/`:

1. Ensure the package has a clear, single responsibility
2. Include comprehensive README.md with usage examples
3. Export a clean public API through index.ts
4. Version changes according to semantic versioning
5. Update CHANGELOG.md with all modifications

#### Cross-Package Dependencies

- Packages should depend on other packages sparingly
- Avoid circular dependencies at all costs
- Document package dependency graph in `docs/architecture/package-dependencies.md`

#### Application Development

When working on applications under `apps/`:

1. Follow the established folder structure:
   ```
   apps/[app-name]/
     src/
       components/    # Application-specific components
       services/      # Business logic and API clients
       hooks/         # Custom React hooks (if applicable)
       utils/         # App-specific utilities
       types/         # Local type definitions
       config/        # Configuration files
     tests/
     public/          # Static assets
   ```

2. Import shared components from `@acme/ui-components`
3. Import shared utilities from `@acme/utils`
4. Keep application-specific code within the app directory

### API Development Standards

For services in `apps/api-gateway/` and `apps/worker-service/`:

- Follow RESTful principles for HTTP APIs
- Use OpenAPI 3.0 specifications stored in `docs/api-specs/`
- Implement proper error handling with standardized error codes
- Use dependency injection for service instantiation
- Validate all inputs using schemas from `@acme/data-models`

### Database and Data Layer

- All database schemas are defined in `packages/data-models/src/schemas/`
- Use migrations for schema changes (stored in respective app's `migrations/` directory)
- Abstract database access behind repository patterns
- Never expose raw database queries in API controllers

### Environment Configuration

- Environment variables are documented in `docs/configuration.md`
- Each app has its own `.env.example` file
- Shared configuration constants live in `packages/config/`
- Use different configs for: development, staging, production

## Build and Development

### Monorepo Commands

- `npm run build` - Build all packages and applications
- `npm run build:packages` - Build only shared packages
- `npm run test` - Run all tests across the monorepo
- `npm run test:watch` - Run tests in watch mode
- `npm run lint` - Lint all code
- `npm run lint:fix` - Auto-fix linting issues

### Working with Individual Apps

To work on a specific application:

```bash
cd apps/web-dashboard
npm run dev          # Start development server
npm run test        # Run app-specific tests
npm run build       # Build for production
```

### Package Development Workflow

When modifying a shared package:

1. Make changes to the package code
2. Run package tests: `npm run test` (from package directory)
3. Build the package: `npm run build`
4. Test in consuming apps before committing
5. Update version and CHANGELOG

## Git Workflow

### Branch Naming Convention

- `feature/[ticket-id]-brief-description` - New features
- `fix/[ticket-id]-brief-description` - Bug fixes
- `refactor/[component-name]` - Code refactoring
- `docs/[topic]` - Documentation updates
- `chore/[task]` - Maintenance tasks

### Commit Messages

Follow conventional commits:
- `feat(web-dashboard): add user profile page`
- `fix(ui-components): resolve button alignment issue`
- `refactor(utils): optimize date formatting function`
- `test(api-gateway): add integration tests for auth`
- `docs(architecture): update deployment diagram`

### Pull Request Guidelines

- Title should follow commit message format
- Include issue/ticket reference in description
- List affected apps and packages
- Provide testing instructions
- Request review from package owners when modifying shared code
- Ensure CI passes before merging

## CI/CD Pipeline

### Continuous Integration

Our CI pipeline (`.github/workflows/ci.yml`) runs:
1. Dependency installation
2. Linting across all projects
3. Type checking
4. Unit and integration tests
5. Build verification
6. Security scanning

### Deployment Strategy

- **Shared Packages**: Published to private npm registry on merge to main
- **Applications**: Deployed based on change detection
  - `web-dashboard`: Deploys to Vercel
  - `mobile-app`: Builds and publishes to app stores
  - `api-gateway` & `worker-service`: Deploy to Kubernetes cluster

### Change Detection

Only affected applications are deployed:
- Changes in `packages/*` trigger builds for all consuming apps
- Changes in `apps/web-dashboard/*` only trigger web-dashboard deployment
- Changes in `infrastructure/*` trigger infrastructure updates

## Security Practices

1. **Secrets Management**: Never commit secrets; use environment variables and secret management services
2. **Dependency Scanning**: Regularly run `npm audit` and address vulnerabilities
3. **Code Review**: All changes require review from at least one team member
4. **Authentication**: Use OAuth 2.0 / OIDC for user authentication
5. **Authorization**: Implement RBAC (Role-Based Access Control) consistently

## Performance Considerations

- **Bundle Size**: Monitor bundle sizes for web and mobile apps
- **Code Splitting**: Implement lazy loading for routes and heavy components
- **Shared Package Size**: Keep shared packages lean; don't include unnecessary dependencies
- **Caching**: Implement appropriate caching strategies at API and UI levels

## Documentation Requirements

When making changes, update relevant documentation:

- README.md files in modified packages/apps
- API specifications in `docs/api-specs/` for API changes
- Architecture diagrams in `docs/architecture/` for structural changes
- Runbooks in `docs/runbooks/` for operational changes

## Common Tasks

### Adding a New Shared Package

1. Create directory under `packages/[package-name]`
2. Initialize with package.json using workspace naming convention
3. Set up tsconfig.json inheriting from root config
4. Create src/index.ts as entry point
5. Add README.md with purpose and usage
6. Add to root package.json workspaces if needed
7. Update package dependency documentation

### Adding a New Application

1. Create directory under `apps/[app-name]`
2. Initialize with appropriate framework scaffolding
3. Configure to use shared packages from workspace
4. Add to CI/CD pipeline configuration
5. Create deployment configuration in `infrastructure/`
6. Document in `docs/architecture/`

### Upgrading Dependencies

1. Check impact across all workspace projects
2. Update in root package.json for shared dependencies
3. Test each application individually
4. Run full test suite
5. Update lock file
6. Document breaking changes if any

## Troubleshooting

### Common Issues

**Issue**: Changes to shared package not reflecting in app
- **Solution**: Rebuild the package and restart the app dev server

**Issue**: Type errors after pulling latest changes
- **Solution**: Run `npm install` from root to ensure all dependencies are linked

**Issue**: Build failures in CI but works locally
- **Solution**: Verify all dependencies are in package.json, not just installed locally

## Team Practices

- **Code Ownership**: Each package and app has designated owners listed in CODEOWNERS file
- **Sync Meetings**: Architecture changes are discussed in weekly sync meetings
- **RFC Process**: Significant architectural changes require RFC in `docs/rfcs/`
- **Knowledge Sharing**: Document learnings and patterns in team wiki

## References

- [Monorepo Architecture Overview](./docs/architecture/monorepo-design.md)
- [Package Development Guide](./docs/guides/package-development.md)
- [Deployment Runbook](./docs/runbooks/deployment.md)
- [Troubleshooting Guide](./docs/guides/troubleshooting.md)

---

**Note**: This is a living document. Update it as the monorepo structure and practices evolve.
