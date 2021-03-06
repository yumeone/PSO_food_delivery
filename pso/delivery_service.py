
from pso.system import *

class Courier:

    def __init__(self, order_list: List[Order]) -> None:
        self._order_list = order_list
        self.max_bag_weight = 18
        self._bag: List[Order] = []
    pass

    def get_path(self, timetable):
        path, fitness = self.calculate_route(timetable=timetable)
        return path

    def fitness(self, timetable):
        path, fitness = self.calculate_route(timetable=timetable)
        return fitness

    @property
    def order_list(self):
        return self._order_list

    @order_list.setter
    def order_list(self, new_list):
        self.order_list = new_list

    pass

    @property
    def bag(self):
        return self._bag

    @bag.setter
    def bag(self, bag):
        self._bag = bag

    def bag_weight(self) -> float:
        """
        Calculates the total weight of the bag
        :return: total_weight
        """
        return sum([x.weight for x in self.bag])

    def update_delivery_time(self, time: float) -> None:
        """

        :param time: time to add
        :return: None
        """
        if self.bag:
            for order in self.bag:
                order.time_in_bag += time

    def calculate_route(self, timetable: TimeTable) -> Tuple[List[Stop], float]:
        """
        Choosing path based on orders order using greedy programming tactics.
        :param timetable: table containing travel time between points
        :return: Courier path, cost of the path


        """


        path: List[Stop] = []
        cost: float = 0
        i=0

        start_order: Order = self._order_list[0]
        self.bag.append(start_order)
        path.append(start_order.source)
        # 1.
        for order_in_source in start_order.source.order_list:
            if order_in_source.id is not start_order.id:
                if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                    self.bag.append(order_in_source)
        # 2.
        for order_from_list in self._order_list[1:]:


            # 2a
            if order_from_list in self.bag:
                for order_in_bag in self.bag:
                    if order_in_bag.id is not order_from_list.id:
                        step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        path.append(order_in_bag.destination)
                        self.update_delivery_time(step_length)
                        cost += step_length
                        self.bag.remove(order_in_bag)


                    else:

                        step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        path.append(order_in_bag.destination)
                        self.update_delivery_time(step_length)
                        cost += step_length
                        self.bag.remove(order_in_bag)



            # 2b
            else:
                #1
                if len(self.bag) > 0:

                    for order_in_bag in self.bag:
                        order_in_bag_step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                        if order_in_bag_step_length < order_in_list_step_length:
                            path.append(order_in_bag.destination)
                            cost += order_in_bag_step_length
                            self.update_delivery_time(order_in_bag_step_length)
                            self.bag.remove(order_in_bag)

                        else:
                            if self.bag_weight() + order_from_list.weight < self.max_bag_weight:
                                path.append(order_from_list.source)
                                self.update_delivery_time(order_in_list_step_length)
                                cost += order_in_list_step_length
                                self.bag.append(order_from_list)

                                for order_in_source in order_from_list.source.order_list:
                                    if order_in_source.id is not order_from_list.id:
                                        if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                            self.bag.append(order_in_source)
                                break


                            else:
                                path.append(order_in_bag.destination)
                                cost += order_in_bag_step_length
                                self.update_delivery_time(order_in_bag_step_length)
                                self.bag.remove(order_in_bag)


                    if order_from_list not in self.bag:
                        order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                        path.append(order_from_list.source)
                        self.update_delivery_time(order_in_list_step_length)
                        cost += order_in_list_step_length
                        self.bag.append(order_from_list)

                        for order_in_source in order_from_list.source.order_list:
                            if order_in_source.id is not order_from_list.id:
                                if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                    self.bag.append(order_in_source)


                #2
                else:

                    order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                    path.append(order_from_list.source)
                    cost += order_in_list_step_length
                    self.bag.append(order_from_list)

                    for order_in_source in order_from_list.source.order_list:
                        if order_in_source.id is not order_from_list.id:
                            if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                self.bag.append(order_in_source)



        if len(self.bag) > 0:


            for order_in_bag in self.bag:
                order_in_bag_step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                path.append(order_in_bag.destination)
                cost += order_in_bag_step_length
                self.update_delivery_time(order_in_bag_step_length)

                #self.bag.remove(order_in_bag)

            self.bag = []
        return path, cost

    def draw_route(self, timetable: TimeTable, ax: plt.axes, index: int, colour: str = 'red') -> plt.axes:
        c = 'red' if isinstance(self.get_path(timetable)[0], Restaurant) else "blue"
        ax.scatter(self.get_path(timetable)[0].cords[0], self.get_path(timetable)[0].cords[1], c=c)
        ax.annotate("START", (self.get_path(timetable)[0].cords[0], self.get_path(timetable)[0].cords[1] + 0.1))
        ax.annotate(str(self.get_path(timetable)[0]), (self.get_path(timetable)[0].cords[0], self.get_path(timetable)[0].cords[1]))

        for idx, point in enumerate(self.get_path(timetable)[:-1]):
            c = 'red' if isinstance(point, Restaurant) else "blue"
            ax.scatter(self.get_path(timetable)[idx+1].cords[0], self.get_path(timetable)[idx+1].cords[1], c=c)
            ax.annotate(str(self.get_path(timetable)[idx+1]), (self.get_path(timetable)[idx+1].cords[0], self.get_path(timetable)[idx+1].cords[1]))
            #draw_line(point, self.get_path(timetable)[idx+1], timetable, colour=colour,ax = ax)

        x= [i.cords[0] for i in self.get_path(timetable)]
        y= [i.cords[1] for i in self.get_path(timetable)]
        ax.plot(x,y,label=f'Courier {index}')

        return ax






