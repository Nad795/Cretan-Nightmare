class Fin:
    def __init__(self, cols, rows, grid_cells):
        self.finish_cell = self.calculate_exit(cols, rows, grid_cells)

    @staticmethod
    def calculate_exit(cols, rows, grid_cells):
        # Start DFS from a cell other than (0, 0) to avoid placing the exit there
        start_cell = grid_cells[1]  # Start from the second cell
        stack = [start_cell]
        visited = set()
        farthest_cell = start_cell
        max_distance = 0

        while stack:
            current = stack.pop()
            visited.add((current.x, current.y))

            # Calculate Manhattan distance from (0, 0)
            distance = abs(current.x - 0) + abs(current.y - 0)
            if distance > max_distance:  # Update farthest cell
                max_distance = distance
                farthest_cell = current

            # Add neighbors to the stack
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = current.x + dx, current.y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    neighbor = grid_cells[ny * cols + nx]
                    if (neighbor.x, neighbor.y) not in visited and not neighbor.visited:
                        stack.append(neighbor)

        # Make sure the exit isn't at the start cell
        if farthest_cell.x == 0 and farthest_cell.y == 0:
            # If the farthest cell ends up being (0, 0), we need to find the next farthest one
            stack = [grid_cells[1]]  # Re-run DFS starting from the second cell
            visited.clear()
            farthest_cell = stack[0]
            max_distance = 0

            while stack:
                current = stack.pop()
                visited.add((current.x, current.y))

                distance = abs(current.x - 0) + abs(current.y - 0)
                if distance > max_distance:
                    max_distance = distance
                    farthest_cell = current

                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = current.x + dx, current.y + dy
                    if 0 <= nx < cols and 0 <= ny < rows:
                        neighbor = grid_cells[ny * cols + nx]
                        if (neighbor.x, neighbor.y) not in visited and not neighbor.visited:
                            stack.append(neighbor)

        return farthest_cell
