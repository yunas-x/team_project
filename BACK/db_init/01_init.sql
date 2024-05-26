CREATE TYPE public."competencetype" AS ENUM (
	'UNIVERSAL',
	'GENERAL_PROFESSIONAL',
	'PROFESSIONAL');

CREATE TYPE public."coursetype" AS ENUM (
	'MANDATORY',
	'ELECTIVE',
	'FACULTATIVE');

CREATE TABLE public."Competence" (
	id serial4 NOT NULL,
	code varchar NOT NULL,
	competence_type public."competencetype" NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT "Competence_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Competence_competence_type" ON public."Competence" USING btree (competence_type);
CREATE INDEX "ix_Competence_id" ON public."Competence" USING btree (id);

CREATE TABLE public."Course" (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	"type" public."coursetype" NOT NULL,
	added date NULL,
	removed date NULL,
	CONSTRAINT "Course_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Course_id" ON public."Course" USING btree (id);
CREATE INDEX "ix_Course_type" ON public."Course" USING btree (type);

CREATE TABLE public."Degree" (
	id int4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT "Degree_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Degree_id" ON public."Degree" USING btree (id);

CREATE TABLE public."Faculty" (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT "Faculty_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Faculty_id" ON public."Faculty" USING btree (id);

CREATE TABLE public."FieldOfStudy" (
	field_code varchar NOT NULL,
	field_group_code varchar NULL,
	field_name varchar NOT NULL,
	CONSTRAINT "FieldOfStudy_pkey" PRIMARY KEY (field_code),
	CONSTRAINT "FieldOfStudy_field_group_code_fkey" FOREIGN KEY (field_group_code) REFERENCES public."FieldOfStudy"(field_code)
);
CREATE INDEX "ix_FieldOfStudy_field_code" ON public."FieldOfStudy" USING btree (field_code);
CREATE INDEX "ix_FieldOfStudy_field_group_code" ON public."FieldOfStudy" USING btree (field_group_code);
CREATE INDEX "ix_FieldOfStudy_field_name" ON public."FieldOfStudy" USING btree (field_name);

CREATE TABLE public."Program" (
	id serial4 NOT NULL,
	program_name varchar NOT NULL,
	CONSTRAINT "Program_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Program_id" ON public."Program" USING btree (id);

CREATE TABLE public."University" (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT "University_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_University_id" ON public."University" USING btree (id);
CREATE INDEX "ix_University_name" ON public."University" USING btree (name);

CREATE TABLE public."Curricula" (
	id serial4 NOT NULL,
	course_id int4 NOT NULL,
	competence_id int4 NOT NULL,
	program_id int4 NOT NULL,
	degree_id int4 NOT NULL,
	field_code varchar NOT NULL,
	university_id int4 NOT NULL,
	faculty_id int4 NOT NULL,
	enrollment_year date NOT NULL,
	"year" int4 NOT NULL,
	credits int4 NOT NULL,
	classroom_hours int4 NULL,
	CONSTRAINT "Curricula_pkey" PRIMARY KEY (id)
);
CREATE INDEX "ix_Curricula_enrollment_year" ON public."Curricula" USING btree (enrollment_year);
CREATE INDEX "ix_Curricula_year" ON public."Curricula" USING btree (year);


-- public."Curricula" foreign keys

ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_competence_id_fkey" FOREIGN KEY (competence_id) REFERENCES public."Competence"(id);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_course_id_fkey" FOREIGN KEY (course_id) REFERENCES public."Course"(id);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_degree_id_fkey" FOREIGN KEY (degree_id) REFERENCES public."Degree"(id);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_faculty_id_fkey" FOREIGN KEY (faculty_id) REFERENCES public."Faculty"(id);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_field_code_fkey" FOREIGN KEY (field_code) REFERENCES public."FieldOfStudy"(field_code);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_program_id_fkey" FOREIGN KEY (program_id) REFERENCES public."Program"(id);
ALTER TABLE public."Curricula" ADD CONSTRAINT "Curricula_university_id_fkey" FOREIGN KEY (university_id) REFERENCES public."University"(id);
