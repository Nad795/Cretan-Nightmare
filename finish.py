class Fin:
    def __init__(self, cols, rows, grid_cells):
        # Avoid finish being at (0,0) by checking the calculated exit point
        self.finish_cell = self.calculate_exit(cols, rows, grid_cells)

    @staticmethod
    def calculate_exit(cols, rows, grid_cells):
        # Avoid (0, 0) as a finish point if needed, and ensure the maze has been generated
        start_cell = grid_cells[0]
        stack = [start_cell]
        visited = set()
        farthest_cell = start_cell
        max_distance = 0

        while stack:
            current = stack.pop()
            visited.add((current.x, current.y))

            # Calculate Manhattan distance from (0, 0)
            distance = abs(current.x - 0) + abs(current.y - 0)
            if distance > max_distance and (current.x, current.y) != (0, 0):  # Exclude (0, 0)
                max_distance = distance
                farthest_cell = current

            # Add neighbors to the stack
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    neighbor = grid_cells[ny * cols + nx]
                    if (neighbor.x, neighbor.y) not in visited and neighbor.visited:
                        stack.append(neighbor)

        return farthest_cell
