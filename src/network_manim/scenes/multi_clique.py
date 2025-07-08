from manim import *  # Manim’s public API

# Local helpers
from ..config import (FPS, NODE_RADIUS, EDGE_WIDTH, COLORS)
from ..graph_utils import (
    CustomDot, circular_image_node, replace_dot_list, build_edge, build_clique,  # ← to implement
)

class MultiCliqueAnimated7(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.image_nodes = []

        # Define edge colors for recoloring steps
        edge_color = BLACK if self.camera.background_color == WHITE else WHITE
        edge_color_1 = ManimColor("#F75969")#ORANGE # Type 1: within-clique edges (middle + left), default is YELLOW
        edge_color_2 = ManimColor("#F9D35A")#PINK # Type 2: interlinks among left cliques and middle, # default is RED
        edge_color_3 = ManimColor("#6ECC82")#BS381.BRILLIANT_GREEN        # Type 3: within right cliques, # default is TEAL
        edge_color_4 = ManimColor("#5CAAEA")#BS381.AZURE_BLUE        # Type 4: X to right-clique nodes, # default is PINK

        # Define per-clique final node colors
        color_sds   = ManimColor("#C4D08D")   #BS381.GOLDEN_YELLOW# MAROON # default is BLUE
        color_bio   = ManimColor("#F28BB6")#BS381.BOLD_GREEN #GREEN_B # default is GREEN
        color_stat  = ManimColor("#E4C2B9")#BS381.AIRCRAFT_BLUE#BLUE_B # default is YELLOW
        color_mstat = ManimColor("#BD8EBF")#BS381.IMPERIAL_BROWN #TEAL_B # default is PURPLE
        color_fam   = ManimColor("#8593C9")#RED_B # default is RED
        color_fr    = ManimColor("#ACD8CF")#YELLOW_B # default is ORANGE
        color_sfam  = ManimColor("#8CABAB")#PURPLE_B # default is PINK

        # Define group‐level node colors (temporary for clustering)
        color_middle_group = MAROON
        color_left_group   = GOLD
        color_right_group  = LIGHT_PINK

        node_radius = NODE_RADIUS
        edge_opacity = EDGE_OPACITY

        # ─────────────────────────────────────────────────────────────────────
        # 1) Build SDS clique (middle) at full size, edges initially WHITE

        labels_sds = ["X", "Y"] + [f"Y{i+1}" for i in range(6)]
        num_sds = len(labels_sds)  # 8
        full_radius = 2.0

        # Compute full-size circle positions (centered at origin)
        base_angles = [0, PI]
        extra_angles = [2 * PI * k / 8 for k in [1, 2, 3, 5, 6, 7]]
        angles_sds = base_angles + extra_angles
        positions_sds_full = [
            full_radius * np.array([np.cos(a), np.sin(a), 0]) for a in angles_sds
        ]

        # Compressed positions (half-size) at origin
        positions_sds_compressed = [pos * 0.5 for pos in positions_sds_full]
        # Right-shifted (compressed + shift)
        shift_right = 4 * RIGHT
        positions_sds_right = [pos + shift_right for pos in positions_sds_compressed]

        # Create X at origin, move to full-size
        x_dot = CustomDot("X").move_to(ORIGIN) # Dot(ORIGIN, radius=node_radius, color=GREY)
        self.image_nodes.append(x_dot)  # Store for later recoloring
        if SHOW_LABELS:
            x_label = Text("X").scale(0.5).next_to(x_dot, UP, buff=0.08)
            x_group = VGroup(x_dot, x_label)
        else:
            x_group = Group(x_dot)
        self.play(FadeIn(x_group), run_time=0.5)
        self.wait(2)
        self.play(x_group.animate.move_to(positions_sds_full[0]), run_time=0.8)
        self.wait(1)

        # Create Y off-screen left, move to full-size
        y_target_full = positions_sds_full[1]
        y_initial = y_target_full + LEFT * 2
        y_dot = CustomDot("Y").move_to(y_initial)#Dot(y_initial, radius=node_radius, color=GREY)
        self.image_nodes.append(y_dot)  # Store for later recoloring
        if SHOW_LABELS:
            y_label = Text("Y").scale(0.5).next_to(y_dot, UP, buff=0.08)
            y_group = VGroup(y_dot, y_label)
        else:
            y_group = Group(y_dot)
        self.play(FadeIn(y_group), run_time=0.5)
        self.play(y_group.animate.move_to(y_target_full), run_time=0.8)
        self.wait(1)

        # Draw initial SDS edge X–Y in WHITE
        A = x_dot.get_center()
        B = y_dot.get_center()
        unit = (B - A) / np.linalg.norm(B - A)
        start_xy = A + unit * node_radius
        end_xy   = B - unit * node_radius
        edge_xy = Line(start_xy, end_xy, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
        self.play(Create(edge_xy), run_time=0.5)
        self.wait(1)

        if SHOW_LABELS:
            self.bring_to_front(x_label, y_label)

        # Build Y1…Y6 around full-size circle, edges WHITE
        sds_dots = [x_dot, y_dot]
        sds_labels = [x_label if SHOW_LABELS else None, y_label if SHOW_LABELS else None]
        sds_edges = [edge_xy]

        for idx in range(2, num_sds):
            label = labels_sds[idx]
            pos_full = positions_sds_full[idx]
            dot = CustomDot(label).move_to(pos_full)#Dot(pos_full, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.5).next_to(dot, UP, buff=0.08)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            sds_dots.append(dot)
            sds_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in sds_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.25)
                sds_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        # ─────────────────────────────────────────────────────────────────────
        # 2) Compress SDS clique and move to the right (nodes+labels+edges)

        label_offsets = []
        for dot, lbl in zip(sds_dots, sds_labels):
            if SHOW_LABELS and lbl:
                label_offsets.append(lbl.get_center() - dot.get_center())
            else:
                label_offsets.append(None)

        moves = []
        for i, dot in enumerate(sds_dots):
            new_pos = positions_sds_right[i]
            moves.append(dot.animate.move_to(new_pos))
            if SHOW_LABELS and sds_labels[i]:
                target_lbl_pos = new_pos + label_offsets[i]
                moves.append(sds_labels[i].animate.move_to(target_lbl_pos))

        edge_moves = []
        edge_indices = [(i, j) for i in range(len(sds_dots)) for j in range(i+1, len(sds_dots))]
        for edge, (i, j) in zip(sds_edges, edge_indices):
            new_A = positions_sds_right[i]
            new_B = positions_sds_right[j]
            unit = (new_B - new_A) / np.linalg.norm(new_B - new_A)
            start = new_A + unit * node_radius
            end   = new_B - unit * node_radius
            edge_moves.append(edge.animate.put_start_and_end_on(start, end))

        self.play(*moves, *edge_moves, run_time=1.0)
        self.wait(0.3)

        # Title “SDS” above compressed clique
        compressed_top_y = full_radius * 0.75 + 0.3
        title_sds = Text("SDS").set_color(edge_color).scale(0.6).move_to(np.array([shift_right[0], compressed_top_y, 0]))
        self.play(FadeIn(title_sds), run_time=0.5)
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 3) Build left cliques: BioStat, Stat, MStat (edges WHITE)

        # BioStat clique (8) top-left
        labels_bio = [f"BIO{i+1}" for i in range(5)]
        num_bio = len(labels_bio)
        center_bio = np.array([-3.5,  2.5, 0])
        radius_bio = 1.0

        bio_dots = []
        bio_labels = []
        bio_edges = []

        for i, label in enumerate(labels_bio):
            angle = 2 * PI * i / num_bio
            pos = center_bio + radius_bio * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)# Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, LEFT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            bio_dots.append(dot)
            bio_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.2)
            self.wait(0.2)

            for prev_dot in bio_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.1)
                bio_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        # Stat clique (3) mid-left
        labels_stat = [f"STAT{i+1}" for i in range(3)]
        num_stat = len(labels_stat)
        center_stat = np.array([-3.5,  0.0, 0])
        radius_stat = 0.8

        stat_dots = []
        stat_labels = []
        stat_edges = []

        for i, label in enumerate(labels_stat):
            angle = 2 * PI * i / num_stat
            pos = center_stat + radius_stat * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)# Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, LEFT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            stat_dots.append(dot)
            stat_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in stat_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.2)
                stat_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        # MStat clique (8) bottom-left
        labels_mstat = [f"MStat{i+1}" for i in range(5)]
        num_mstat = len(labels_mstat)
        center_mstat = np.array([-3.5, -2.5, 0])
        radius_mstat = 1.0

        mstat_dots = []
        mstat_labels = []
        mstat_edges = []

        for i, label in enumerate(labels_mstat):
            angle = 2 * PI * i / num_mstat
            pos = center_mstat + radius_mstat * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)# Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, LEFT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            mstat_dots.append(dot)
            mstat_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in mstat_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.2)
                mstat_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        # Titles for left cliques
        fixed_left_x = center_bio[0] - radius_bio - 1.5
        title_bio = Text("BioStat").set_color(edge_color).scale(0.6).move_to(np.array([fixed_left_x, center_bio[1], 0]))
        title_bio.align_to(title_bio.get_left(), LEFT)
        self.play(FadeIn(title_bio), run_time=0.5)
        self.wait(0.5)

        title_stat = Text("Stat").set_color(edge_color).scale(0.6).move_to(np.array([fixed_left_x, center_stat[1], 0]))
        title_stat.align_to(title_stat.get_left(), LEFT)
        self.play(FadeIn(title_stat), run_time=0.5)
        self.wait(0.5)

        title_mstat = Text("MStat").set_color(edge_color).scale(0.6).move_to(np.array([fixed_left_x, center_mstat[1], 0]))
        title_mstat.align_to(title_mstat.get_left(), LEFT)
        self.play(FadeIn(title_mstat), run_time=0.5)
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 4) Add cross‐links among SDS and left cliques + left-left (Type2 candidates), edges WHITE

        type2_edges = []  # store (edge, ep1_info, ep2_info)
        cross_pairs = [
            (0, bio_dots[0]),    # X–BIO1
            (2, stat_dots[0]),   # Y1–STAT1
            (3, mstat_dots[0]),  # Y2–MStat1
            (bio_dots[1], stat_dots[1]),   # BIO2–STAT2
            (4, bio_dots[2]),    # Y3–BIO3
            (5, mstat_dots[1]),  # Y4–MStat2
            (mstat_dots[2], stat_dots[2]), # MStat3–STAT3
            (bio_dots[3], 6),    # BIO4–Y5
            (mstat_dots[3], bio_dots[4]),  # MStat4–BIO5
            (stat_dots[1], 7),   # STAT2–Y6
            (mstat_dots[4], bio_dots[4]),  # MStat5–BIO6
            (bio_dots[2], stat_dots[0]),   # BIO7–STAT1
            (6, mstat_dots[4]),  # Y5–MStat6
            (mstat_dots[3], bio_dots[2]),  # MStat7–BIO8
            (stat_dots[2], 5),   # STAT3–Y4
        ]

        for pair in cross_pairs:
            def endpoint_info(elem):
                if isinstance(elem, int):
                    return ("sds", elem)
                elif elem in bio_dots:
                    return ("bio", bio_dots.index(elem))
                elif elem in stat_dots:
                    return ("stat", stat_dots.index(elem))
                else:
                    return ("mstat", mstat_dots.index(elem))

            ep1 = endpoint_info(pair[0])
            ep2 = endpoint_info(pair[1])

            if ep1[0] == "sds":
                A = sds_dots[ep1[1]].get_center()
            elif ep1[0] == "bio":
                A = bio_dots[ep1[1]].get_center()
            elif ep1[0] == "stat":
                A = stat_dots[ep1[1]].get_center()
            else:
                A = mstat_dots[ep1[1]].get_center()

            if ep2[0] == "sds":
                B = sds_dots[ep2[1]].get_center()
            elif ep2[0] == "bio":
                B = bio_dots[ep2[1]].get_center()
            elif ep2[0] == "stat":
                B = stat_dots[ep2[1]].get_center()
            else:
                B = mstat_dots[ep2[1]].get_center()

            unit = (B - A) / np.linalg.norm(B - A)
            start = A + unit * node_radius
            end   = B - unit * node_radius
            edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
            self.play(Create(edge), run_time=0.1)
            #self.wait(0.1)
            type2_edges.append((edge, ep1, ep2))
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 5) Move SDS clique back to center (still compressed),
        #    and move Type2 edges accordingly

        moves_back = []
        for i, dot in enumerate(sds_dots):
            target_pos = positions_sds_compressed[i]
            moves_back.append(dot.animate.move_to(target_pos))
            if SHOW_LABELS and sds_labels[i]:
                target_lbl_pos = target_pos + label_offsets[i]
                moves_back.append(sds_labels[i].animate.move_to(target_lbl_pos))
        # now add the title to move back as well:
        # compute its new x-position (centered = 0) and same vertical offset
        new_title_sds_pos = np.array([0, compressed_top_y, 0])
        moves_back.append(title_sds.animate.move_to(new_title_sds_pos))

        edge_moves_back = []
        for edge_obj, (i, j) in zip(sds_edges, edge_indices):
            new_A = positions_sds_compressed[i]
            new_B = positions_sds_compressed[j]
            unit = (new_B - new_A) / np.linalg.norm(new_B - new_A)
            start = new_A + unit * node_radius
            end   = new_B - unit * node_radius
            edge_moves_back.append(edge_obj.animate.put_start_and_end_on(start, end))

        type2_moves = []
        for edge_obj, ep1, ep2 in type2_edges:
            if ep1[0] == "sds":
                new_A = positions_sds_compressed[ep1[1]]
            elif ep1[0] == "bio":
                new_A = bio_dots[ep1[1]].get_center()
            elif ep1[0] == "stat":
                new_A = stat_dots[ep1[1]].get_center()
            else:
                new_A = mstat_dots[ep1[1]].get_center()

            if ep2[0] == "sds":
                new_B = positions_sds_compressed[ep2[1]]
            elif ep2[0] == "bio":
                new_B = bio_dots[ep2[1]].get_center()
            elif ep2[0] == "stat":
                new_B = stat_dots[ep2[1]].get_center()
            else:
                new_B = mstat_dots[ep2[1]].get_center()

            unit = (new_B - new_A) / np.linalg.norm(new_B - new_A)
            start = new_A + unit * node_radius
            end   = new_B - unit * node_radius
            type2_moves.append(edge_obj.animate.put_start_and_end_on(start, end))

        self.play(*moves_back, *edge_moves_back, *type2_moves, run_time=1.0)
        self.wait(0.5)

        # ─────────────────────────────────────────────────────────────────────
        # 6) Build right cliques: Fam, Fr, SFam (edges WHITE)

        # Fam clique (8) top-right
        labels_fam = [f"Fam{i+1}" for i in range(7)]
        num_fam = len(labels_fam)
        center_fam = np.array([3.5,  2.5, 0])
        radius_fam = 1.0
        fixed_right_x = center_fam[0] + radius_fam + 1.5

        fam_dots = []
        fam_labels = []
        fam_edges = []

        for i, label in enumerate(labels_fam):
            angle = 2 * PI * i / num_fam
            pos = center_fam + radius_fam * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)#Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, RIGHT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            fam_dots.append(dot)
            fam_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in fam_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.2)
                fam_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        title_fam = Text("Famille").set_color(edge_color).scale(0.6).move_to(np.array([fixed_right_x, center_fam[1], 0]))
        title_fam.align_to(title_fam.get_right(), RIGHT)
        self.play(FadeIn(title_fam), run_time=0.5)
        self.wait(0.5)

        # Fr clique (10) mid-right (radius=0.9)
        labels_fr = [f"Fr{i+1}" for i in range(8)]
        num_fr = len(labels_fr)
        center_fr = np.array([3.5,  0.0, 0])
        radius_fr = 0.9

        fr_dots = []
        fr_labels = []
        fr_edges = []

        for i, label in enumerate(labels_fr):
            angle = 2 * PI * i / num_fr
            pos = center_fr + radius_fr * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)# Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, RIGHT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            fr_dots.append(dot)
            fr_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in fr_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.18)
                fr_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        title_fr = Text("Amis").set_color(edge_color).scale(0.6).move_to(np.array([fixed_right_x, center_fr[1], 0]))
        title_fr.align_to(title_fr.get_right(), RIGHT)
        self.play(FadeIn(title_fr), run_time=0.5)
        self.wait(0.5)

        # SFam clique (5) bottom-right
        labels_sfam = [f"SFam{i+1}" for i in range(5)]
        num_sfam = len(labels_sfam)
        center_sfam = np.array([3.5, -2.5, 0])
        radius_sfam = 0.8

        sfam_dots = []
        sfam_labels = []
        sfam_edges = []

        for i, label in enumerate(labels_sfam):
            angle = 2 * PI * i / num_sfam
            pos = center_sfam + radius_sfam * np.array([np.cos(angle), np.sin(angle), 0])
            dot = CustomDot(label).move_to(pos)#Dot(pos, radius=node_radius, color=GREY)
            self.image_nodes.append(dot)  # Store for later recoloring
            if SHOW_LABELS:
                lbl = Text(label).scale(0.4).next_to(dot, RIGHT, buff=0.1)
                grp = VGroup(dot, lbl)
            else:
                grp = Group(dot)
                lbl = None

            sfam_dots.append(dot)
            sfam_labels.append(lbl)
            self.play(FadeIn(grp), run_time=0.4)
            self.wait(0.2)

            for prev_dot in sfam_dots[:-1]:
                A = prev_dot.get_center()
                B = dot.get_center()
                unit = (B - A) / np.linalg.norm(B - A)
                start = A + unit * node_radius
                end   = B - unit * node_radius
                edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
                self.play(Create(edge), run_time=0.2)
                sfam_edges.append(edge)

            if SHOW_LABELS:
                self.bring_to_front(lbl)
            self.wait(0.2)

        title_sfam = Text("B-Famille").set_color(edge_color).scale(0.6).move_to(np.array([fixed_right_x, center_sfam[1], 0]))
        title_sfam.align_to(title_sfam.get_right(), RIGHT)
        self.play(FadeIn(title_sfam), run_time=0.5)
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 7) Link X to every node in the right cliques (Type4 candidates), edges WHITE

        type4_edges = []
        for dot in (fam_dots + fr_dots + sfam_dots):
            A = x_dot.get_center()
            B = dot.get_center()
            unit = (B - A) / np.linalg.norm(B - A)
            start = A + unit * node_radius
            end   = B - unit * node_radius
            edge = Line(start, end, stroke_width=EDGE_WIDTH, color=edge_color).set_opacity(edge_opacity)
            self.play(Create(edge), run_time=0.3)
            self.wait(0.1)
            type4_edges.append(edge)

        # ─────────────────────────────────────────────────────────────────────
        # Step 7.5: Replace all image nodes with white circular dots at the same positions
        white_nodes = []
        fadeout_animations = []
        fadein_animations = []

        # A mapping from old image nodes to new dot replacements
        replacement_map = {}

        for mob in self.image_nodes:
            if isinstance(mob, ImageMobject):
                white_dot = Dot(mob.get_center(), radius=NODE_RADIUS, color=GREY).set_z_index(1)
                fadeout_animations.append(FadeOut(mob))
                fadein_animations.append(FadeIn(white_dot))
                white_nodes.append(white_dot)
                replacement_map[mob] = white_dot

        if fadeout_animations and fadein_animations:
            self.play(*fadeout_animations, *fadein_animations, run_time=1.5)
            self.wait(2)

        sds_dots   = replace_dot_list(sds_dots, replacement_map)
        bio_dots   = replace_dot_list(bio_dots, replacement_map)
        stat_dots  = replace_dot_list(stat_dots, replacement_map)
        mstat_dots = replace_dot_list(mstat_dots, replacement_map)
        fam_dots   = replace_dot_list(fam_dots, replacement_map)
        fr_dots    = replace_dot_list(fr_dots, replacement_map)
        sfam_dots  = replace_dot_list(sfam_dots, replacement_map)

        # ─────────────────────────────────────────────────────────────────────
        # 8) Recolor all nodes by group: middle, left, right

        # Middle (SDS) → MAROON
        for dot in sds_dots:
            self.play(dot.animate.set_fill(color_middle_group, opacity=1), run_time=0.1)
        # Left (BioStat + Stat + MStat) → GOLD
        for dot in bio_dots + stat_dots + mstat_dots:
            self.play(dot.animate.set_fill(color_left_group, opacity=1), run_time=0.1)
        # Right (Fam + Fr + SFam) → PURPLE_E
        for dot in fam_dots + fr_dots + sfam_dots:
            self.play(dot.animate.set_fill(color_right_group, opacity=1), run_time=0.1)
        self.wait(2.5)

# ─────────────────────────────────────────────────────────────────────
        # 9) Recolor nodes by individual clique

        # SDS → BLUE
        for dot in sds_dots:
            self.play(dot.animate.set_fill(color_sds, opacity=1), run_time=0.1)
        # BioStat → GREEN
        for dot in bio_dots:
            self.play(dot.animate.set_fill(color_bio, opacity=1), run_time=0.1)
        # Stat → YELLOW
        for dot in stat_dots:
            self.play(dot.animate.set_fill(color_stat, opacity=1), run_time=0.1)
        # MStat → PURPLE
        for dot in mstat_dots:
            self.play(dot.animate.set_fill(color_mstat, opacity=1), run_time=0.1)
        # Fam → RED
        for dot in fam_dots:
            self.play(dot.animate.set_fill(color_fam, opacity=1), run_time=0.1)
        # Fr → ORANGE
        for dot in fr_dots:
            self.play(dot.animate.set_fill(color_fr, opacity=1), run_time=0.1)
        # SFam → PINK
        for dot in sfam_dots:
            self.play(dot.animate.set_fill(color_sfam, opacity=1), run_time=0.1)
        self.wait(2.5)

        # ─────────────────────────────────────────────────────────────────────
        # 10) Switch all node colors back to GREY

        all_nodes = sds_dots + bio_dots + stat_dots + mstat_dots + fam_dots + fr_dots + sfam_dots
        for dot in all_nodes:
            self.play(dot.animate.set_fill(GREY, opacity=1), run_time=0.05)
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 11) Recolor edges within-cliques of left and middle (Type1)

        for edge in sds_edges:
            self.play(edge.animate.set_color(edge_color_1), run_time=0.05)
        for edge in bio_edges:
            self.play(edge.animate.set_color(edge_color_1), run_time=0.05)
        for edge in stat_edges:
            self.play(edge.animate.set_color(edge_color_1), run_time=0.05)
        for edge in mstat_edges:
            self.play(edge.animate.set_color(edge_color_1), run_time=0.05)
        self.wait(2)

        legend1_line = Line(np.array([0, 0, 0]), np.array([0.5, 0, 0]),
                            stroke_width=4, color=edge_color_1).set_opacity(edge_opacity)
        legend1_text = Text("IntraLab").set_color(edge_color).set_color(edge_color).scale(0.5).next_to(legend1_line, RIGHT, buff=0.15)
        legend1 = VGroup(legend1_line, legend1_text)

        # ─────────────────────────────────────────────────────────────────────
        # 12) Recolor edges among left cliques and middle (Type2),
        #     including left-left

        for edge_obj, _, _ in type2_edges:
            self.play(edge_obj.animate.set_color(edge_color_2), run_time=0.05)
        self.wait(0.5)

        legend2_line = Line(np.array([0, 0, 0]), np.array([0.5, 0, 0]),
                            stroke_width=4, color=edge_color_2).set_opacity(edge_opacity)
        legend2_text = Text("InterLab").set_color(edge_color).scale(0.5).next_to(legend2_line, RIGHT, buff=0.15)
        legend2 = VGroup(legend2_line, legend2_text)

        # ─────────────────────────────────────────────────────────────────────
        # 13) Recolor edges within right cliques (Type3)

        for edge in fam_edges + fr_edges + sfam_edges:
            self.play(edge.animate.set_color(edge_color_3), run_time=0.05)
        self.wait(0.5)

        legend3_line = Line(np.array([0, 0, 0]), np.array([0.5, 0, 0]),
                            stroke_width=4, color=edge_color_3).set_opacity(edge_opacity)
        legend3_text = Text("IntraProche").set_color(edge_color).scale(0.5).next_to(legend3_line, RIGHT, buff=0.15)
        legend3 = VGroup(legend3_line, legend3_text)

        # ─────────────────────────────────────────────────────────────────────
        # 14) Recolor edges from X to right-clique nodes (Type4)

        for edge in type4_edges:
            self.play(edge.animate.set_color(edge_color_4), run_time=0.05)
        self.wait(0.5)

        legend4_line = Line(np.array([0, 0, 0]), np.array([0.5, 0, 0]),
                            stroke_width=4, color=edge_color_4).set_opacity(edge_opacity)
        legend4_text = Text("InterProche").set_color(edge_color).scale(0.5).next_to(legend4_line, RIGHT, buff=0.15)
        legend4 = VGroup(legend4_line, legend4_text)

        self.wait(5)

        # ─────────────────────────────────────────────────────────────────────
        # 15) Recolor nodes by individual clique (after edges kept colored)

        # SDS → BLUE
        for dot in sds_dots:
            self.play(dot.animate.set_fill(color_sds, opacity=1), run_time=0.1)
        # BioStat → GREEN
        for dot in bio_dots:
            self.play(dot.animate.set_fill(color_bio, opacity=1), run_time=0.1)
        # Stat → YELLOW
        for dot in stat_dots:
            self.play(dot.animate.set_fill(color_stat, opacity=1), run_time=0.1)
        # MStat → PURPLE
        for dot in mstat_dots:
            self.play(dot.animate.set_fill(color_mstat, opacity=1), run_time=0.1)
        # Fam → RED
        for dot in fam_dots:
            self.play(dot.animate.set_fill(color_fam, opacity=1), run_time=0.1)
        # Fr → ORANGE
        for dot in fr_dots:
            self.play(dot.animate.set_fill(color_fr, opacity=1), run_time=0.1)
        # SFam → PINK
        for dot in sfam_dots:
            self.play(dot.animate.set_fill(color_sfam, opacity=1), run_time=0.1)
        self.wait(2.5)

        # ─────────────────────────────────────────────────────────────────────
        # 16) Display combined legend entries without overlap

        all_legends = VGroup(legend1, legend2, legend3, legend4).arrange(RIGHT, buff=1.5)
        # Snap the legend group to the bottom edge with a small buffer
        all_legends.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(all_legends), run_time=0.5)
        self.wait(3)

                # ─────────────────────────────────────────────────────────────────────
        # 17) Fade out every edge
        all_edges = (
            sds_edges
            + bio_edges + stat_edges + mstat_edges
            + fam_edges + fr_edges + sfam_edges
            + [e for e,_,_ in type2_edges]
            + type4_edges
        )
        self.play(*[FadeOut(e) for e in all_edges], run_time=0.5)
        # Fade out the legends too
        self.play(*[FadeOut(leg) for leg in all_legends], run_time=0.5)

        # ─────────────────────────────────────────────────────────────────────
        # 19) Gather and shrink all nodes before layout
        base_nodes = (
            sds_dots
            + bio_dots + stat_dots + mstat_dots
            + fam_dots + fr_dots + sfam_dots
        )
        # Remove *all* labels/titles first
        all_text = (
            [lbl for lbl in sds_labels if lbl]
            + [lbl for lbl in bio_labels+stat_labels+mstat_labels if lbl]
            + [lbl for lbl in fam_labels+fr_labels+sfam_labels if lbl]
            + [x_label if SHOW_LABELS else None, y_label if SHOW_LABELS else None,
               title_sds, title_bio, title_stat, title_mstat,
               title_fam, title_fr, title_sfam]
        )
        self.play(*[FadeOut(txt) for txt in all_text], run_time=0.5)

        # Shrink every node by factor 5
        #tiny_radius = NODE_RADIUS / 5
        #shrink_factor = tiny_radius / NODE_RADIUS
        # Scaling parameter
        node_scaling_factor = 3.0
        tiny_radius = NODE_RADIUS / node_scaling_factor
        shrink_factor = tiny_radius / NODE_RADIUS
        self.play(*[dot.animate.scale(shrink_factor) for dot in base_nodes], run_time=0.5)

        # ─────────────────────────────────────────────────────────────────────
        # 20) Build row+column arrays with X duplicated at start

        # Row: [X] + all nodes
        row_nodes = base_nodes # [base_nodes[0]] +
        # Column: same
        col_nodes = []

        m = len(row_nodes)  # = original n + 1

        # Compute a cell_size so the total span is 50% of the smaller frame dimension
        frame_w = self.camera.frame_width
        frame_h = self.camera.frame_height
        # Cell size based on desired node spacing
        padding = tiny_radius * 1.5
        cell = 2 * tiny_radius# + padding
        span = cell * m

        x0 = -span/2 + cell/2
        margin = 0.2  # space above bottom edge
        y0 = -frame_h / 4 + m* cell - cell / 2 + margin 

        # Optional: cap y0 so it doesn't push grid too far up
        max_y0 = frame_h / 2 - cell  # ensure top row stays in frame
        print(f"max_y0: {max_y0}, y0: {y0}")
        y0 = 3# min(y0, max_y0)
        #y0 = frame_h/2 - frame_h * 0.2
        #span    = min(frame_w, frame_h) * 0.5
        #cell    = span / m

        # Compute the starting x, y0
        #x0 = -span/2 + cell/2
        #y0 = frame_h/2 - frame_h * 0.2

        # Animate the entire row in one go (1s)
        self.play(*[
            dot.animate.move_to([x0 + (i+1)*cell, y0, 0])
            for i, dot in enumerate(row_nodes)
        ], run_time=1.0)

        # Build the column clones and animate in one go
        col_anims = []
        for i, orig in enumerate(row_nodes):
            clone = Dot(orig.get_center(), radius=tiny_radius, color=orig.get_fill_color())
            self.add(clone)
            target = [x0, y0 - (i+1)*cell, 0]
            col_anims.append(clone.animate.move_to(target))
        self.play(*col_anims, run_time=1.0)
# ─────────────────────────────────────────────────────────────────────
        # 21) Draw the closed (m×m) grid *around* the nodes, stroke_width=1

        # Push the grid lines just outside the node borders
        offset = 2*tiny_radius# + cell

        left   = x0 + offset/2
        right  = x0 + (m+1)*cell - offset/2
        top    = y0 - offset/2
        bottom = y0 - (m+1)*cell + offset/2

        grid = VGroup()
        # vertical lines k=0…m
        for k in range(m+1):
            x = left + k*cell
            grid.add(Line([x, top,    0], [x, bottom, 0], stroke_width=1.0, color=GREY))
        # horizontal lines k=0…m
        for k in range(m+1):
            y = top - k*cell
            grid.add(Line([left,  y, 0], [right, y, 0], stroke_width=1.0, color=GREY))

        self.play(Create(grid), run_time=1.0)


        # ─────────────────────────────────────────────────────────────────────
        # Build edge‐pair lists for fast lookup

        # Type 1: all intra‐clique edges in SDS + left cliques
        edge_pairs_type1 = []
        for group in (sds_dots, bio_dots, stat_dots, mstat_dots):
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    edge_pairs_type1.append((group[i], group[j]))

        # Type 2: all cross‐links among SDS and left cliques (and left–left)
        edge_pairs_type2 = []
        for edge_obj, ep1, ep2 in type2_edges:
            def resolve(ep):
                kind, idx = ep
                return {
                    "sds":   sds_dots,
                    "bio":   bio_dots,
                    "stat":  stat_dots,
                    "mstat": mstat_dots,
                }[kind][idx]
            edge_pairs_type2.append((resolve(ep1), resolve(ep2)))

        # Type 3: intra‐clique edges in right‐hand cliques
        edge_pairs_type3 = []
        for group in (fam_dots, fr_dots, sfam_dots):
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    edge_pairs_type3.append((group[i], group[j]))

        # Type 4: edges from X to every node in the right cliques
        x_dot = replacement_map.get(x_dot, x_dot)
        edge_pairs_type4 = [(x_dot, dot) for dot in (fam_dots + fr_dots + sfam_dots)]

        # ─────────────────────────────────────────────────────────────────────
        # The lookup function

        def lookup_edge_type(a, b):
            """
            Returns 1–4 if (a,b) is in the corresponding edge_pairs_typeN list,
            or None if no edge exists.
            """
            if (a, b) in edge_pairs_type1 or (b, a) in edge_pairs_type1:
                return 1
            if (a, b) in edge_pairs_type2 or (b, a) in edge_pairs_type2:
                return 2
            if (a, b) in edge_pairs_type3 or (b, a) in edge_pairs_type3:
                return 3
            if (a, b) in edge_pairs_type4 or (b, a) in edge_pairs_type4:
                return 4
            return None

        # ─────────────────────────────────────────────────────────────────────
        # Build a dot→label mapping for debug prints
        label_map = {}
        # SDS clique
        for dot, name in zip(sds_dots, labels_sds):
            label_map[dot] = name
        # BioStat
        for dot, name in zip(bio_dots, labels_bio):
            label_map[dot] = name
        # Stat
        for dot, name in zip(stat_dots, labels_stat):
            label_map[dot] = name
        # MStat
        for dot, name in zip(mstat_dots, labels_mstat):
            label_map[dot] = name
        # Fam
        for dot, name in zip(fam_dots, labels_fam):
            label_map[dot] = name
        # Fr
        for dot, name in zip(fr_dots, labels_fr):
            label_map[dot] = name
        # SFam
        for dot, name in zip(sfam_dots, labels_sfam):
            label_map[dot] = name

        # ─────────────────────────────────────────────────────────────────────
        # 23) Fill grid pixels white, shifted one cell down so diagonal aligns
        # Store pixels with their edge type for later recoloring
        typed_pixels = []

        # We still use i,j in 0…m-1, skip self‐loops on diagonal
        for i in range(m):
            for j in range(m):
                if i == j:
                    continue
                a = row_nodes[i]
                b = row_nodes[j]
                et = lookup_edge_type(a, b)
                if et is None:
                    continue
                # debug print
                #print(f"Plotting pixel for edge: ({label_map[a]}, {label_map[b]})")
                # now draw the square...


                # center of cell *one down* from the normal (i,j) slot:
                x_center = left  + i*cell + cell/2
                y_center = top   - (j+1)*cell + cell/2

                pix = Square(
                    side_length=cell,
                    fill_color=edge_color,
                    fill_opacity=1.0,
                    stroke_width=0
                ).move_to([x_center, y_center, 0])

                self.play(FadeIn(pix), run_time=0.01)

                typed_pixels.append((pix, et))
        typed_pixels = [
            (new_pix, etype)
            for pix, etype in typed_pixels
            if (new_pix := replacement_map.get(pix, pix)) is not None and isinstance(new_pix, Mobject)
        ]
        self.wait(2)

        # ─────────────────────────────────────────────────────────────────────
        # 24) Recolor pixels by edge type, in one go
        # Define a color map
        color_map = {
            1: edge_color_1,
            2: edge_color_2,
            3: edge_color_3,
            4: edge_color_4,
        }
        for et in [1, 2, 3, 4]:
            self.play(*[
                pix.animate.set_fill(color_map[et], opacity=1.0)
                for pix, et2 in typed_pixels if et2 == et
            ], run_time=0.01)
        # Add the legend for edge types back
        self.play(FadeIn(legend1), FadeIn(legend2), FadeIn(legend3), FadeIn(legend4), run_time=0.5)



        self.wait(5)
